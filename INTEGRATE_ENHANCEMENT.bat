@echo off
chcp 65001 >nul
setlocal

echo =========================================================
echo    UFO³ Galaxy 增强模块一键集成脚本
echo =========================================================
echo.
echo 本脚本将把 UFO³ Galaxy 的增强功能集成到您现有的
echo 微软 UFO 项目中。

echo.
echo [1/4] 检查 Git 是否安装...
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Git！
    echo 请先从 https://git-scm.com/download/win 下载并安装 Git。
    pause
    exit /b 1
)
echo [✓] Git 已安装。

echo.
echo [2/4] 克隆增强模块仓库...
if exist "ufo-galaxy-enhancement" (
    echo [✓] 增强模块已存在，跳过克隆。
) else (
    echo 正在克隆 https://github.com/DannyFish-11/ufo-galaxy.git...
    git clone https://github.com/DannyFish-11/ufo-galaxy.git ufo-galaxy-enhancement
    if %errorlevel% neq 0 (
        echo [错误] 克隆失败！请检查您的网络连接。
        pause
        exit /b 1
    )
    echo [✓] 增强模块克隆成功。
)

echo.
echo [3/4] 复制核心文件和目录...

echo  - 复制一键安装脚本...
copy /Y "ufo-galaxy-enhancement\INSTALL_AND_START.bat" . >nul
copy /Y "ufo-galaxy-enhancement\TEST_SYSTEM.py" . >nul

echo  - 复制 Windows 客户端...
xcopy /E /I /Y "ufo-galaxy-enhancement\windows_client" ".\windows_client" >nul

echo  - 复制云节点...
xcopy /E /I /Y "ufo-galaxy-enhancement\node_60_cloud" ".\node_60_cloud" >nul

echo  - 复制 Podman 容器配置...
xcopy /E /I /Y "ufo-galaxy-enhancement\nodes" ".\nodes" >nul
copy /Y "ufo-galaxy-enhancement\podman-compose.yml" . >nul

echo  - 复制文档...
if not exist "docs" mkdir "docs"
xcopy /E /I /Y "ufo-galaxy-enhancement\docs" ".\docs\ufo-galaxy-enhancement" >nul
copy /Y "ufo-galaxy-enhancement\README_EASY_START.md" ".\docs\" >nul

echo [✓] 文件复制完成。

echo.
echo [4/4] 清理临时文件...
del /F /Q "ufo-galaxy-enhancement\*.*" >nul 2>&1
for /d %%i in ("ufo-galaxy-enhancement\*") do rd /s /q "%%i"
rd "ufo-galaxy-enhancement"
echo [✓] 清理完成。

echo.
echo =========================================================
echo    ✅ 集成成功！
echo =========================================================
echo.
echo 下一步:

echo   1. 右键点击 INSTALL_AND_START.bat

echo   2. 选择 "以管理员身份运行"

echo.
echo 祝您在极客松比赛中取得好成绩！🚀
echo.
echo 按任意键退出...
pause >nul
