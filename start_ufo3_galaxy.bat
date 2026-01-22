@echo off
REM UFO³ Galaxy 一键启动脚本 (Windows)
REM 版本: 1.0
REM 日期: 2026-01-22

echo ========================================
echo  UFO³ Galaxy 启动脚本
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.11
    pause
    exit /b 1
)

echo [1/5] 检查 Python 版本...
python --version

REM 检查 ADB 是否安装
adb version >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到 ADB，部分安卓控制功能可能无法使用
) else (
    echo [2/5] 检查 ADB 版本...
    adb version | findstr "Android"
)

REM 检查 Tailscale 是否运行
tailscale status >nul 2>&1
if errorlevel 1 (
    echo [警告] Tailscale 未运行，跨网络设备通信可能无法使用
) else (
    echo [3/5] Tailscale 状态:
    tailscale status | findstr /C:"100."
)

REM 加载环境变量
if exist .env (
    echo [4/5] 加载环境变量...
    for /f "usebackq tokens=1,* delims==" %%a in (".env") do (
        set "%%a=%%b"
    )
) else (
    echo [警告] 未找到 .env 文件，使用默认配置
)

REM 启动 UFO³ Galaxy
echo [5/5] 启动 UFO³ Galaxy 系统...
echo.
echo 正在启动核心节点和扩展节点...
echo 这可能需要几分钟时间，请耐心等待...
echo.

python galaxy_launcher.py --include-groups core extended

echo.
echo ========================================
echo  UFO³ Galaxy 已停止
echo ========================================
pause
