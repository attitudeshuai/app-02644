# 🔬 科学计算器

Python + Tkinter 科学计算器，现代深色主题界面。

---

## 快速启动

### 一键启动（推荐）

**Windows:**
```cmd
双击 start.bat
```
或
```powershell
.\start.ps1
```

**macOS / Linux:**
```bash
bash start.sh
```

> 脚本会自动检测 Python 和 tkinter，如果缺失会提示安装方法

### 手动运行
```bash
cd calculator
python main.py
```

---

## 功能

| 类别 | 功能 |
|------|------|
| 基础运算 | 加减乘除、括号、百分比、正负切换 |
| 三角函数 | sin, cos, tan（支持 DEG/RAD 切换） |
| 对数函数 | log（常用对数）, ln（自然对数） |
| 幂与开方 | x²、^（任意次幂）、√（平方根） |
| 数学常数 | π, e |
| 辅助功能 | 历史记录、键盘输入、中文错误提示 |

---

## 键盘快捷键

| 按键 | 功能 |
|------|------|
| 0-9, . | 数字输入 |
| + - * / | 运算符 |
| ^ (Shift+6) | 幂运算 |
| Enter | 计算 |
| Backspace | 删除 |
| Escape | 清除 |

> ⚠️ **Mac 用户注意：** Mac 键盘 Control (⌃) 键上印有 `^` 符号，但该键是系统修饰键，用于触发系统快捷键（如 ⌃+Space 切换输入法、⌃+C 终止进程等），无法用于输入幂运算符。请使用 `Shift+6` 或点击界面上的 `^` 按钮来输入幂运算。

---

## 项目结构

```
├── start.bat             # Windows 一键启动
├── start.ps1             # Windows PowerShell 启动
├── start.sh              # macOS/Linux 一键启动
└── calculator/
    ├── main.py           # 入口
    ├── tests/            # 单元测试
    └── calculator/
        ├── app.py        # 主应用
        ├── engine.py     # 计算引擎
        ├── parser.py     # 安全表达式解析器
        └── ui/           # 界面组件
```

---

## 运行测试

```bash
cd calculator
python -m unittest discover tests/ -v
```

---

## 技术栈

- Python 3.8+
- Tkinter（内置 GUI 库）
- 无外部依赖


## License

MIT
