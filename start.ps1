# 科学计算器一键启动脚本 (Windows PowerShell)

Write-Host "========================================"
Write-Host "  科学计算器 - 一键启动"
Write-Host "========================================"
Write-Host ""

# 查找 Python
function Find-Python {
    $pythonCmds = @("python", "python3", "py")
    foreach ($cmd in $pythonCmds) {
        try {
            $version = & $cmd --version 2>&1
            if ($version -match "Python 3") {
                return $cmd
            }
        } catch {}
    }
    return $null
}

$python = Find-Python

if (-not $python) {
    Write-Host "[错误] 未找到 Python 3" -ForegroundColor Red
    Write-Host ""
    Write-Host "请从以下地址下载安装 Python:" -ForegroundColor Yellow
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "安装时请勾选:" -ForegroundColor Yellow
    Write-Host "  - 'Add Python to PATH'" -ForegroundColor White
    Write-Host "  - 'tcl/tk and IDLE'" -ForegroundColor White
    Write-Host ""
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Host "[OK] Python: $(& $python --version)" -ForegroundColor Green

# 检查 tkinter
Write-Host ""
Write-Host "[信息] 检查 tkinter..."
try {
    & $python -c "import tkinter" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "[OK] tkinter 可用" -ForegroundColor Green
} catch {
    Write-Host "[错误] tkinter 不可用" -ForegroundColor Red
    Write-Host ""
    Write-Host "请重新安装 Python 并勾选 'tcl/tk and IDLE'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "按 Enter 键退出"
    exit 1
}

# 切换到脚本目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$scriptDir\calculator"

# 启动应用
Write-Host ""
Write-Host "========================================"
Write-Host "[信息] 启动计算器..."
Write-Host "========================================"
& $python main.py
