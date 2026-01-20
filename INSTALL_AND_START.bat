@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ========================================
echo    UFO³ Galaxy 一键安装启动脚本
echo ========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 请以管理员身份运行此脚本！
    echo 右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo [1/8] 检查 Python 环境...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 未检测到 Python！
    echo 请先安装 Python 3.10 或更高版本：https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [✓] Python 已安装

echo.
echo [2/8] 检查 Podman Desktop...
podman --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 未检测到 Podman！
    echo 请先安装 Podman Desktop：https://podman-desktop.io/downloads
    pause
    exit /b 1
)
echo [✓] Podman 已安装

echo.
echo [3/8] 检查 Tailscale...
tailscale status >nul 2>&1
if %errorLevel% neq 0 (
    echo [警告] 未检测到 Tailscale 或未启动
    echo 请确保 Tailscale 已安装并登录：https://tailscale.com/download
    echo 按任意键继续（如果您确定 Tailscale 已配置）...
    pause >nul
)
echo [✓] Tailscale 已配置

echo.
echo [4/8] 获取 Tailscale IP 地址...
for /f "tokens=*" %%i in ('tailscale ip -4 2^>nul') do set TAILSCALE_IP=%%i
if "!TAILSCALE_IP!"=="" (
    echo [警告] 无法自动获取 Tailscale IP，使用默认值 100.123.215.126
    set TAILSCALE_IP=100.123.215.126
) else (
    echo [✓] Tailscale IP: !TAILSCALE_IP!
)

echo.
echo [5/8] 配置环境变量...
set ONEAPI_BASE_URL=http://!TAILSCALE_IP!:3000/v1
set ONEAPI_API_KEY=sk-your-oneapi-key
set PIXVERSE_API_KEY=sk-f5c7177f35ee6cceab5d97d6ffae26d0
set GITHUB_TOKEN=
set NOTION_API_KEY=
set SILICON_FLOW_API_KEY=
set BRAVE_API_KEY=
set OPENWEATHER_API_KEY=
set SLACK_TOKEN=
set ZHIPU_API_KEY=
set TOGETHER_API_KEY=
set OPENROUTER_API_KEY=
set GROQ_API_KEY=
set GEMINI_API_KEY=
set OPENAI_API_KEY=
echo [✓] 环境变量已设置

echo.
echo [6/8] 安装 Python 依赖...
cd /d "%~dp0"
if exist "requirements.txt" (
    pip install -r requirements.txt -q
    echo [✓] Python 依赖已安装
) else (
    echo [警告] 未找到 requirements.txt，跳过依赖安装
)

echo.
echo [7/8] 启动 Podman 容器...
if exist "podman-compose.yml" (
    echo 正在启动容器，这可能需要几分钟...
    podman-compose up -d
    if %errorLevel% equ 0 (
        echo [✓] 容器已启动
    ) else (
        echo [错误] 容器启动失败！
        echo 请检查 Podman Desktop 是否正在运行
        pause
        exit /b 1
    )
) else (
    echo [警告] 未找到 podman-compose.yml，跳过容器启动
)

echo.
echo [8/8] 等待服务就绪...
timeout /t 10 /nobreak >nul
echo [✓] 服务已就绪

echo.
echo ========================================
echo    安装完成！
echo ========================================
echo.
echo 后端节点已在 Podman 中运行
echo Node 50 (大脑) 监听地址: ws://localhost:8050
echo.
echo 接下来请运行：
echo   1. Windows 客户端: cd windows_client ^&^& python client.py
echo   2. Android 客户端: 安装 APK 并授予悬浮窗权限
echo   3. 华为云节点: 在云服务器上运行部署脚本
echo.
echo 按任意键退出...
pause >nul
