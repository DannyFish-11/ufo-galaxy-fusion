@echo off
REM UFO³ Galaxy 系统启动脚本
REM 作者：Manus AI
REM 日期：2026-01-23

echo ================================================================================
echo UFO³ Galaxy 系统启动
echo ================================================================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装或不在 PATH 中
    echo 请安装 Python 3.11+ 并添加到 PATH
    pause
    exit /b 1
)

echo 请选择启动模式：
echo.
echo 1. 核心系统（Core）
echo 2. 学术研究系统（Academic）
echo 3. 开发工作流系统（Development）
echo 4. 完整系统（All）
echo 5. 查看系统状态
echo 6. 退出
echo.

set /p choice=请输入选项 (1-6): 

if "%choice%"=="1" (
    echo.
    echo 启动核心系统...
    python system_manager.py start --group core
) else if "%choice%"=="2" (
    echo.
    echo 启动学术研究系统...
    python system_manager.py start --group academic
) else if "%choice%"=="3" (
    echo.
    echo 启动开发工作流系统...
    python system_manager.py start --group development
) else if "%choice%"=="4" (
    echo.
    echo 启动完整系统...
    python system_manager.py start --group all
) else if "%choice%"=="5" (
    echo.
    echo 检查系统状态...
    python system_manager.py status
    echo.
    pause
    goto :eof
) else if "%choice%"=="6" (
    echo.
    echo 退出
    goto :eof
) else (
    echo.
    echo [错误] 无效的选项
    pause
    goto :eof
)
