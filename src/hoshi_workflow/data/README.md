# 数据资源访问功能

## 概述

`hoshi_workflow` 现在包含了一个 `data` 子模块，可以安全地访问包内的数据文件（如 `stable.txt`），无论用户在哪个目录运行代码。

## 快速开始

### 安装

```bash
cd /path/to/HOSHI_WorkFlow
pip install -e .
```

### 基本使用

```python
from hoshi_workflow.data import get_stable_isotopes_path, load_stable_isotopes

# 方法 1: 获取文件路径
path = get_stable_isotopes_path()
print(f"stable.txt 位于: {path}")

# 方法 2: 直接加载解析后的数据
isotopes = load_stable_isotopes()
for A, Z, element, abundance in isotopes['data'][:5]:
    print(f"{element}-{A}: {abundance:.2e}")
```

## 文件结构

```
src/hoshi_workflow/
├── __init__.py
├── data/
│   ├── __init__.py          # 数据访问 API
│   └── solar/
│       └── stable.txt       # 太阳稳定同位素数据
├── hoshi_reader/
│   └── hoshi_reader.py
└── ...
```

## API 函数

### `get_data_path()`
返回 data 目录的绝对路径。

### `get_stable_isotopes_path()`
返回 stable.txt 文件的绝对路径。

### `load_stable_isotopes()`
加载并解析 stable.txt 文件，返回：
```python
{
    'data': [(A, Z, element, abundance), ...],  # 列表of元组
    'path': Path('/path/to/stable.txt')         # 文件路径
}
```

## 示例

### 在 Pandas 中使用

```python
import pandas as pd
from hoshi_workflow.data import get_stable_isotopes_path

path = get_stable_isotopes_path()
df = pd.read_csv(path, sep=r'\s+', names=['A', 'Z', 'Element', 'Abundance'])
df = df[df['Element'] != 'end']
print(df.head())
```

### 创建查找字典

```python
from hoshi_workflow.data import load_stable_isotopes

isotopes = load_stable_isotopes()
lookup = {
    f"{elem}-{A}": abundance 
    for A, Z, elem, abundance in isotopes['data']
}

print(f"H-1 abundance: {lookup['H-1']:.2e}")
print(f"Fe-56 abundance: {lookup['Fe-56']:.2e}")
```

## 测试

运行测试以验证功能：

```bash
python tests/test_data_access.py
```

查看完整示例：

```bash
python examples/example_accessing_stable_data.py
```

## 文档

详细文档请参阅：
- [docs/accessing_stable_data.md](../docs/accessing_stable_data.md) - 完整使用指南
- [examples/example_accessing_stable_data.py](../examples/example_accessing_stable_data.py) - 代码示例

## 为什么这样设计？

### 问题
以前的代码可能使用硬编码路径：
```python
# ❌ 不推荐：硬编码路径
file_path = '/data/home/user/HOSHI/data/solar/stable.txt'
```

这种方式有以下问题：
1. **不可移植**: 在其他机器上路径无效
2. **安装后失效**: pip 安装后路径会改变
3. **难以维护**: 每个用户需要修改代码

### 解决方案
使用 `hoshi_workflow.data` 模块：
```python
# ✅ 推荐：使用包资源访问
from hoshi_workflow.data import get_stable_isotopes_path
file_path = get_stable_isotopes_path()
```

优点：
- ✓ **可移植**: 任何环境都能工作
- ✓ **安装友好**: pip 安装后自动可用
- ✓ **零配置**: 用户无需修改路径
- ✓ **类型安全**: 返回 `pathlib.Path` 对象

## 技术实现

1. **数据文件打包**: 通过 `pyproject.toml` 配置
   ```toml
   [tool.setuptools.package-data]
   hoshi_workflow = ["data/**/*.txt", "data/**/*.dat"]
   ```

2. **路径解析**: 使用 `__file__` 定位模块位置
   ```python
   def get_data_path():
       return Path(__file__).resolve().parent
   ```

3. **错误处理**: 文件不存在时抛出清晰的错误信息

## 添加更多数据文件

要添加新的数据文件：

1. 将文件放入 `src/hoshi_workflow/data/` 的适当子目录
2. 在 `src/hoshi_workflow/data/__init__.py` 中添加访问函数
3. 数据文件会自动包含在包发布中

示例：
```python
# 在 src/hoshi_workflow/data/__init__.py 中
def get_yields_table_path():
    """获取产额表文件路径."""
    return get_data_path() / "yields" / "nomoto2013.txt"
```

## 向后兼容

旧代码可以继续工作，但建议迁移到新 API：

```python
# 旧代码（仍然可用但不推荐）
import os
HOSHI_DIR = os.getenv("HOSHI_DIR")
stable_path = f"{HOSHI_DIR}/data/solar/stable.txt"

# 新代码（推荐）
from hoshi_workflow.data import get_stable_isotopes_path
stable_path = get_stable_isotopes_path()
```

## 常见问题

**Q: 我需要设置环境变量吗？**  
A: 不需要。数据文件访问完全自动化。

**Q: 在 Jupyter Notebook 中可以使用吗？**  
A: 可以！只要安装了包就能在任何地方使用。

**Q: 开发模式（editable install）下能工作吗？**  
A: 能。使用 `pip install -e .` 安装后立即可用。

**Q: 数据文件会被包含在 wheel 包中吗？**  
A: 会。`pyproject.toml` 中的 `package-data` 配置确保数据文件被打包。

## 更新日期

2026年1月16日
