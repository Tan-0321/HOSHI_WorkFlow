# HOSHI WorkFlow 数据访问功能更新

## 更新日期
2026年1月16日

## 问题描述

用户询问如何在 hoshi_reader 中访问 stable 数据文件，并确保在任意路径下使用 hoshireader 库时都能正常访问。

之前的问题：
- 数据文件 `stable.txt` 位于项目根目录的 `data/solar/` 下
- 某些示例代码使用硬编码的绝对路径（如 `/data/home/ktakahashi/HOSHI_210703/data/solar/stable.txt`）
- 用户在不同目录运行代码时无法访问数据文件
- pip 安装后路径会改变，导致访问失败

## 解决方案

实现了完整的包数据资源访问系统：

### 1. 数据文件迁移
- ✅ 将 `stable.txt` 复制到包内部：`src/hoshi_workflow/data/solar/stable.txt`
- ✅ 原文件保留用于向后兼容

### 2. 创建数据访问模块
- ✅ 新建 `src/hoshi_workflow/data/__init__.py`
- ✅ 提供统一的 API 访问数据文件：
  - `get_data_path()` - 获取 data 目录路径
  - `get_stable_isotopes_path()` - 获取 stable.txt 路径
  - `load_stable_isotopes()` - 加载并解析数据
  - `get_solar_stable_path()` - 向后兼容别名

### 3. 包配置更新
- ✅ 更新 `pyproject.toml` 添加 `package-data` 配置
- ✅ 更新 `src/hoshi_workflow/__init__.py` 导出 data 模块

### 4. 文档和示例
- ✅ 创建详细文档：`docs/accessing_stable_data.md`
- ✅ 创建使用示例：`examples/example_accessing_stable_data.py`
- ✅ 创建测试：`tests/test_data_access.py`
- ✅ 创建 README：`src/hoshi_workflow/data/README.md`

## 使用方法

### 基本用法

```python
from hoshi_workflow.data import get_stable_isotopes_path, load_stable_isotopes

# 方法 1: 获取文件路径
path = get_stable_isotopes_path()
with open(path, 'r') as f:
    content = f.read()

# 方法 2: 直接加载数据
isotopes = load_stable_isotopes()
data = isotopes['data']  # [(A, Z, element, abundance), ...]
```

### 在 pandas 中使用

```python
import pandas as pd
from hoshi_workflow.data import get_stable_isotopes_path

path = get_stable_isotopes_path()
df = pd.read_csv(path, sep=r'\s+', names=['A', 'Z', 'Element', 'Abundance'])
```

### 创建查找字典

```python
from hoshi_workflow.data import load_stable_isotopes

isotopes = load_stable_isotopes()
lookup = {f"{elem}-{A}": abundance for A, Z, elem, abundance in isotopes['data']}
print(lookup['H-1'])    # 2.79e+10
print(lookup['Fe-56'])  # 8.25e+05
```

## 技术实现细节

### 文件结构
```
src/hoshi_workflow/
├── data/
│   ├── __init__.py          # 数据访问 API
│   ├── README.md            # 数据模块文档
│   └── solar/
│       └── stable.txt       # 太阳稳定同位素数据
```

### 路径解析机制
使用 `__file__` 属性定位模块位置：
```python
def get_data_path() -> Path:
    this_dir = Path(__file__).resolve().parent
    return this_dir
```

这种方法的优点：
- ✓ 开发模式（`pip install -e .`）下工作
- ✓ 安装模式（`pip install .`）下工作
- ✓ 在任意工作目录下都能访问
- ✓ 不依赖环境变量

### 包数据配置
在 `pyproject.toml` 中：
```toml
[tool.setuptools.package-data]
hoshi_workflow = ["data/**/*.txt", "data/**/*.dat"]
```

确保数据文件被包含在：
- 源码分发包（sdist）
- wheel 包（bdist_wheel）

## 测试验证

### 所有测试通过 ✅

```bash
$ python tests/test_data_access.py
============================================================
Testing hoshi_workflow.data module
============================================================

✓ Import test: PASS
✓ Path access test: PASS
✓ Data loading test: PASS
✓ File content test: PASS

Total: 4/4 tests passed
```

### 跨目录访问验证 ✅

```bash
$ cd /tmp && python -c "from hoshi_workflow.data import ..."
✓ 成功从 /tmp 目录访问数据文件
  路径: /home/tanby/repos/HOSHI_WorkFlow/src/hoshi_workflow/data/solar/stable.txt
  加载了 286 个同位素
```

## 文件清单

### 新建文件
1. `src/hoshi_workflow/data/__init__.py` - 数据访问 API（118行）
2. `src/hoshi_workflow/data/README.md` - 数据模块文档
3. `src/hoshi_workflow/data/solar/stable.txt` - 数据文件副本
4. `docs/accessing_stable_data.md` - 详细使用指南
5. `examples/example_accessing_stable_data.py` - 使用示例
6. `tests/test_data_access.py` - 测试脚本

### 修改文件
1. `pyproject.toml` - 添加 package-data 配置
2. `src/hoshi_workflow/__init__.py` - 导出 data 模块

## 优势

### 用户体验
- ✅ **零配置**: 无需设置环境变量或修改路径
- ✅ **跨平台**: Windows/Linux/Mac 都能工作
- ✅ **位置无关**: 在任何目录运行都能访问
- ✅ **开发友好**: 开发模式和安装模式都支持

### 代码质量
- ✅ **类型提示**: 使用 `pathlib.Path` 和类型注解
- ✅ **错误处理**: 清晰的错误信息
- ✅ **文档完整**: API 文档、示例、测试齐全
- ✅ **向后兼容**: 不破坏现有代码

### 可扩展性
- ✅ **易于扩展**: 添加新数据文件只需两步
- ✅ **统一接口**: 所有数据文件使用相同模式
- ✅ **模块化**: data 模块独立，不影响其他模块

## 迁移指南

### 旧代码（不推荐）
```python
# 硬编码路径
file_path = '/data/home/ktakahashi/HOSHI_210703/data/solar/stable.txt'

# 或依赖环境变量
import os
HOSHI_DIR = os.getenv("HOSHI_DIR")
file_path = f"{HOSHI_DIR}/data/solar/stable.txt"
```

### 新代码（推荐）
```python
from hoshi_workflow.data import get_stable_isotopes_path
file_path = get_stable_isotopes_path()
```

## 未来改进建议

1. **添加更多数据文件**
   - 其他太阳丰度表（如 Asplund 2009）
   - 核反应网络文件
   - 产额表

2. **增强功能**
   - 数据缓存机制
   - 数据验证和校验和
   - 支持远程数据源

3. **性能优化**
   - 延迟加载
   - 二进制格式选项

## 参考资料

- 使用指南: [docs/accessing_stable_data.md](../docs/accessing_stable_data.md)
- 使用示例: [examples/example_accessing_stable_data.py](../examples/example_accessing_stable_data.py)
- 测试脚本: [tests/test_data_access.py](../tests/test_data_access.py)
- 模块文档: [src/hoshi_workflow/data/README.md](../src/hoshi_workflow/data/README.md)

## 结论

通过创建 `hoshi_workflow.data` 模块，我们成功解决了数据文件访问的可移植性问题。用户现在可以在任意路径下使用 hoshireader 库，无需担心数据文件路径配置。这个解决方案遵循 Python 包开发的最佳实践，提供了清晰的 API、完整的文档和充分的测试。
