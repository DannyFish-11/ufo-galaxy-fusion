@echo off
REM UFO³ Galaxy 一键部署脚本
REM 作者：Manus AI
REM 日期：2026-01-23

echo ================================================================================
echo UFO³ Galaxy 一键部署
echo ================================================================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装或不在 PATH 中
    echo.
    echo 请访问 https://www.python.org/downloads/ 下载并安装 Python 3.11+
    pause
    exit /b 1
)

echo [1/6] 检查 Python 版本...
python --version
echo.

REM 检查 pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [错误] pip 未安装
    pause
    exit /b 1
)

echo [2/6] 安装核心依赖...
pip install fastapi uvicorn httpx pydantic -q
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo [成功] 核心依赖已安装
echo.

echo [3/6] 检查 ADB (可选)...
adb version >nul 2>&1
if errorlevel 1 (
    echo [警告] ADB 未安装（安卓设备控制需要）
    echo 如需使用安卓设备，请访问 https://developer.android.com/studio/releases/platform-tools
) else (
    echo [成功] ADB 已安装
)
echo.

echo [4/6] 检查 Tailscale (可选)...
tailscale version >nul 2>&1
if errorlevel 1 (
    echo [警告] Tailscale 未安装（跨设备通信需要）
    echo 如需跨设备通信，请访问 https://tailscale.com/download
) else (
    echo [成功] Tailscale 已安装
)
echo.

echo [5/6] 检查 Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo [警告] Git 未安装
    echo 建议安装 Git 以便更新代码
) else (
    echo [成功] Git 已安装
)
echo.

echo [6/6] 运行环境检查脚本...
python check_environment.py
if errorlevel 1 (
    echo [警告] 环境检查发现问题，请查看上方输出
)
echo.

echo ================================================================================
echo 部署完成！
echo ================================================================================
echo.
echo 下一步：
echo.
echo 1. 启动系统：
echo    start_system.bat
echo.
echo 2. 启动学术系统：
echo    start_academic_system.bat
echo.
echo 3. 启动知识库和 GitHub 工作流：
echo    start_knowledge_github_nodes.bat
echo.
echo 4. 查看系统状态：
echo    python system_manager.py status
echo.
echo 5. 启动健康监控（Web 仪表板）：
echo    python health_monitor.py
echo    然后访问 http://localhost:9000
echo.
echo 6. 安卓设备配置：
echo    查看 ANDROID_QUICK_INSTALL.md
echo.
echo 完整文档：
echo    - QUICKSTART.md (快速开始)
echo    - DEPLOYMENT_GUIDE_UFO3_GALAXY.md (详细部署指南)
echo    - FINAL_DEPLOYMENT_CHECKLIST.md (部署清单)
echo.
pause
