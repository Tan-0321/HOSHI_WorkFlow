"""
快速参考：hoshi_workflow.data 模块

作者: Bingyang Tan
日期: 2026-01-16
"""

# ============================================================
# 1. 导入模块
# ============================================================
from hoshi_workflow.data import (
    get_stable_isotopes_path,    # 获取 stable.txt 路径
    load_stable_isotopes,         # 加载并解析数据
    get_data_path,                # 获取 data/ 目录路径
)

# ============================================================
# 2. 获取文件路径（最常用）
# ============================================================
path = get_stable_isotopes_path()
print(path)  # /path/to/hoshi_workflow/data/solar/stable.txt

# 使用路径读取文件
with open(path, 'r') as f:
    content = f.read()

# ============================================================
# 3. 加载解析后的数据
# ============================================================
isotopes = load_stable_isotopes()
# 返回: {'data': [(A, Z, element, abundance), ...], 'path': Path(...)}

for A, Z, elem, abund in isotopes['data'][:5]:
    print(f"{elem}-{A} (Z={Z}): {abund:.2e}")

# ============================================================
# 4. Pandas DataFrame
# ============================================================
import pandas as pd

path = get_stable_isotopes_path()
df = pd.read_csv(
    path,
    sep=r'\s+',
    names=['A', 'Z', 'Element', 'Abundance']
)
df = df[df['Element'] != 'end'].dropna()

# 处理 Fortran 科学记数法 (2.79d+10 -> 2.79e+10)
df['Abundance'] = df['Abundance'].astype(str).str.replace('d', 'e', case=False)
df['Abundance'] = pd.to_numeric(df['Abundance'], errors='coerce')

# ============================================================
# 5. 创建查找字典
# ============================================================
isotopes = load_stable_isotopes()
lookup = {
    f"{elem}-{A}": abundance 
    for A, Z, elem, abundance in isotopes['data']
}

# 查询特定同位素
h1_abundance = lookup['H-1']      # 2.79e+10
fe56_abundance = lookup['Fe-56']  # 8.25e+05

# ============================================================
# 6. NumPy 数组
# ============================================================
import numpy as np

isotopes = load_stable_isotopes()
data = isotopes['data']

# 提取特定列
mass_numbers = np.array([A for A, Z, elem, abund in data])
atomic_numbers = np.array([Z for A, Z, elem, abund in data])
abundances = np.array([abund for A, Z, elem, abund in data])

# ============================================================
# 7. 过滤特定元素
# ============================================================
isotopes = load_stable_isotopes()

# 获取所有铁同位素
iron_isotopes = [
    (A, abundance) 
    for A, Z, elem, abundance in isotopes['data']
    if elem == 'Fe'
]

print("铁的稳定同位素:")
for A, abund in iron_isotopes:
    print(f"  Fe-{A}: {abund:.2e}")

# ============================================================
# 8. 在类中使用（例如 HoshiProfile）
# ============================================================
from hoshi_workflow.data import load_stable_isotopes

class MyAnalyzer:
    def __init__(self):
        # 在初始化时加载一次
        isotopes = load_stable_isotopes()
        self.solar_abundance = {
            f"{elem}-{A}": abund
            for A, Z, elem, abund in isotopes['data']
        }
    
    def compare_with_solar(self, isotope_name, model_abundance):
        """比较模型丰度与太阳丰度"""
        if isotope_name in self.solar_abundance:
            solar = self.solar_abundance[isotope_name]
            ratio = model_abundance / solar
            return ratio
        return None

# ============================================================
# 9. 错误处理
# ============================================================
try:
    path = get_stable_isotopes_path()
    isotopes = load_stable_isotopes()
except FileNotFoundError as e:
    print(f"数据文件未找到: {e}")
    # 处理错误...

# ============================================================
# 10. 检查数据文件位置
# ============================================================
from hoshi_workflow.data import get_data_path

data_dir = get_data_path()
print(f"数据目录: {data_dir}")
print(f"solar 子目录: {data_dir / 'solar'}")
print(f"stable.txt: {data_dir / 'solar' / 'stable.txt'}")

# ============================================================
# 常见问题 FAQ
# ============================================================

# Q: 需要设置环境变量吗？
# A: 不需要，完全自动化

# Q: 在任何目录都能用吗？
# A: 是的，无论当前工作目录在哪

# Q: pip 安装后还能用吗？
# A: 是的，数据文件会被打包进 wheel

# Q: 开发模式 (pip install -e .) 能用吗？
# A: 能，立即可用

# Q: 性能如何？
# A: get_path() 很快（只是路径查找）
#    load_data() 第一次调用需要解析文件（~0.1秒）
#    建议在程序初始化时加载一次，然后复用

# ============================================================
# 完整示例：分析元素丰度
# ============================================================

def analyze_solar_abundances():
    """完整示例：分析太阳丰度数据"""
    import pandas as pd
    from hoshi_workflow.data import load_stable_isotopes
    
    # 加载数据
    isotopes = load_stable_isotopes()
    
    # 转为 DataFrame
    df = pd.DataFrame(
        isotopes['data'],
        columns=['A', 'Z', 'Element', 'Abundance']
    )
    
    # 统计
    print(f"总同位素数: {len(df)}")
    print(f"元素种类数: {df['Element'].nunique()}")
    
    # 最丰富的10个同位素
    print("\n最丰富的10个同位素:")
    top10 = df.nlargest(10, 'Abundance')
    for _, row in top10.iterrows():
        print(f"  {row['Element']}-{row['A']}: {row['Abundance']:.2e}")
    
    # 按元素分组
    by_element = df.groupby('Element')['Abundance'].sum().sort_values(ascending=False)
    print(f"\n最丰富的10个元素:")
    for elem, total_abund in by_element.head(10).items():
        print(f"  {elem}: {total_abund:.2e}")

if __name__ == "__main__":
    analyze_solar_abundances()
