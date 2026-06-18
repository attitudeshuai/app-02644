@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1
title Scientific Calculator

echo ========================================
echo   Scientific Calculator - Start
echo ========================================
echo.

:: Find Python
set PYTHON=

where python >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set VER=%%i
    echo !VER! | findstr /C:"Python 3" >nul
    if !errorlevel! equ 0 (
        set PYTHON=python
    )
)

if "!PYTHON!"=="" (
    where py >nul 2>&1
    if !errorlevel! equ 0 (
        set PYTHON=py
    )
)

if "!PYTHON!"=="" (
    echo [ERROR] Python 3 not found
    echo.
    echo Please download Python from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check:
    echo   - "Add Python to PATH"
    echo   - "tcl/tk and IDLE"
    echo.
    pause
    exit /b 1
)

echo [OK] Found Python
!PYTHON! --version

:: Check tkinter
echo.
echo Checking tkinter...
!PYTHON! -c "import tkinter" >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] tkinter not available
    echo.
    echo Please reinstall Python and check "tcl/tk and IDLE"
    echo.
    pause
    exit /b 1
)
echo [OK] tkinter available

:: Start application
echo.
echo ========================================
echo Starting calculator...
echo ========================================
cd /d "%~dp0calculator"
!PYTHON! main.py

if !errorlevel! neq 0 (
    echo.
    echo [ERROR] Application error
    pause
)

endlocal
