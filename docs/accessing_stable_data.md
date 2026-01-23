# 访问 Stable Isotopes 数据文件

## 概述

`hoshi_workflow` 包现在包含了太阳丰度的稳定同位素数据文件 (`stable.txt`)，并提供了简便的API来访问它。无论包是在开发模式还是安装模式，无论用户在哪个目录下运行代码，都能正确访问到这个数据文件。

## 安装

确保安装了最新版本的包：

```bash
pip install -e .
```

## 使用方法

### 方法 1: 获取文件路径

```python
from hoshi_workflow.data import get_stable_isotopes_path

# 获取 stable.txt 的绝对路径
stable_path = get_stable_isotopes_path()
print(f"stable.txt 位于: {stable_path}")

# 直接使用这个路径读取文件
with open(stable_path, 'r') as f:
    content = f.read()
    print(content[:200])  # 打印前200个字符
```

### 方法 2: 直接加载数据

```python
from hoshi_workflow.data import load_stable_isotopes

# 加载并解析 stable.txt 数据
isotopes = load_stable_isotopes()

# 访问数据
print(f"数据源: {isotopes['path']}")
print(f"共有 {len(isotopes['data'])} 个稳定同位素")

# 查看前几个同位素
for A, Z, element, abundance in isotopes['data'][:10]:
    print(f"{element}-{A} (Z={Z}): abundance = {abundance:.2e}")
```

### 方法 3: 在 pandas 中使用

```python
import pandas as pd
from hoshi_workflow.data import get_stable_isotopes_path

# 读取为 DataFrame
stable_path = get_stable_isotopes_path()
df = pd.read_csv(
    stable_path,
    sep=r'\s+',
    names=['A', 'Z', 'Element', 'Abundance'],
    comment='#'
)

# 过滤掉 'end' 行
df = df[df['Element'] != 'end']

print(df.head(10))
print(f"\n总共 {len(df)} 个同位素")

# 按元素分组统计
element_counts = df.groupby('Element').size()
print(f"\n每个元素的同位素数量:\n{element_counts.head(10)}")
```

### 方法 4: 在 HoshiReader 中使用

```python
from hoshi_workflow.hoshi_reader import HoshiProfile
from hoshi_workflow.data import load_stable_isotopes

# 加载稳定同位素数据
isotopes_data = load_stable_isotopes()

# 创建一个查找字典
isotope_dict = {
    f"{elem}-{A}": abundance 
    for A, Z, elem, abundance in isotopes_data['data']
}

# 在 profile 中使用
profile = HoshiProfile("/path/to/work_dir", str_num=1000)

# 比较模型中的丰度与太阳丰度
for isotope_name in profile.var_names:
    if isotope_name.startswith('X(') and isotope_name.endswith(')'):
        elem = isotope_name[2:-1]  # 提取元素名称
        if elem in isotope_dict:
            model_abundance = profile.data(isotope_name)
            solar_abundance = isotope_dict[elem]
            print(f"{elem}: model={model_abundance.mean():.2e}, solar={solar_abundance:.2e}")
```

## 数据文件格式

`stable.txt` 文件格式如下：

```
A    Z  Element  Abundance
1    1  H        2.79d+10
2    1  H        9.49d+5
3    2  He       3.86d+5
...
end  0.0
```

- **A**: 质量数
- **Z**: 原子序数
- **Element**: 元素符号
- **Abundance**: 太阳丰度（注意使用 Fortran 格式的科学记数法，如 `2.79d+10`）

## API 参考

### `get_data_path()`
返回 `data/` 目录的绝对路径。

### `get_stable_isotopes_path()`
返回 `stable.txt` 文件的绝对路径。

### `load_stable_isotopes()`
加载并解析 `stable.txt`，返回包含数据列表和文件路径的字典。

返回值结构：
```python
{
    'data': [(A, Z, element, abundance), ...],
    'path': Path('/path/to/stable.txt')
}
```

### `get_solar_stable_path()`
`get_stable_isotopes_path()` 的别名，用于向后兼容。

## 故障排除

### 找不到数据文件

如果遇到 `FileNotFoundError`，请确保：

1. 包已正确安装：`pip install -e .`
2. `src/hoshi_workflow/data/solar/stable.txt` 文件存在
3. 在包的根目录运行安装命令

### 在旧代码中迁移

如果你的旧代码使用硬编码路径：

```python
# 旧方式 (不推荐)
file_path = '/data/home/ktakahashi/HOSHI_210703/data/solar/stable.txt'

# 新方式 (推荐)
from hoshi_workflow.data import get_stable_isotopes_path
file_path = get_stable_isotopes_path()
```

## 添加更多数据文件

如果需要添加其他数据文件：

1. 将文件放入 `src/hoshi_workflow/data/` 的适当子目录
2. 在 `src/hoshi_workflow/data/__init__.py` 中添加访问函数
3. 数据文件会自动包含在包中（因为 `pyproject.toml` 中已配置 `package-data`）
