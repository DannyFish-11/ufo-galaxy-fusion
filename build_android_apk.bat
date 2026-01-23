@echo off
REM UFO³ Galaxy - 安卓端一键打包脚本（增强版）
REM 作者：Manus AI
REM 日期：2026-01-23

setlocal enabledelayedexpansion

echo ================================================================================
echo UFO³ Galaxy - 安卓端一键打包
echo ================================================================================
echo.

REM 检查是否在正确的目录
if not exist "enhancements\clients\android_client" (
    echo [错误] 请在 ufo-galaxy 根目录下运行此脚本
    pause
    exit /b 1
)

cd enhancements\clients\android_client

REM 检查 Gradle
where gradle >nul 2>&1
if errorlevel 1 (
    echo [警告] Gradle 未安装，将使用 gradlew
    if not exist "gradlew.bat" (
        echo [错误] gradlew.bat 不存在
        echo.
        echo 请访问 https://gradle.org/install/ 安装 Gradle
        pause
        exit /b 1
    )
    set GRADLE_CMD=gradlew.bat
) else (
    set GRADLE_CMD=gradle
)

echo [1/5] 获取 PC 的 Tailscale IP...
echo.

REM 检查 Tailscale
tailscale version >nul 2>&1
if errorlevel 1 (
    echo [警告] Tailscale 未安装
    echo.
    set /p PC_IP="请手动输入 PC 的 IP 地址: "
) else (
    REM 自动获取 Tailscale IP
    for /f "tokens=*" %%i in ('tailscale ip -4') do set PC_IP=%%i
    echo 检测到 Tailscale IP: !PC_IP!
    echo.
    set /p CONFIRM="是否使用此 IP？(Y/n): "
    if /i "!CONFIRM!"=="n" (
        set /p PC_IP="请手动输入 PC 的 IP 地址: "
    )
)

echo.
echo [2/5] 选择设备类型...
echo.
echo 1. 小米 14
echo 2. OPPO 平板
echo 3. 自定义设备 ID
echo.
set /p DEVICE_CHOICE="请选择设备类型 (1-3): "

if "!DEVICE_CHOICE!"=="1" (
    set DEVICE_ID=xiaomi-14
    set DEVICE_NAME=小米14
) else if "!DEVICE_CHOICE!"=="2" (
    set DEVICE_ID=oppo-tablet
    set DEVICE_NAME=OPPO平板
) else if "!DEVICE_CHOICE!"=="3" (
    set /p DEVICE_ID="请输入自定义设备 ID: "
    set DEVICE_NAME=!DEVICE_ID!
) else (
    echo [错误] 无效的选择
    pause
    exit /b 1
)

echo.
echo [3/5] 生成配置文件...
echo.

REM 生成配置文件
echo # UFO³ Galaxy Android Client Configuration > app\src\main\assets\config.properties
echo # 自动生成于 %date% %time% >> app\src\main\assets\config.properties
echo. >> app\src\main\assets\config.properties
echo pc.ip=%PC_IP% >> app\src\main\assets\config.properties
echo device.id=%DEVICE_ID% >> app\src\main\assets\config.properties
echo gateway.port=8000 >> app\src\main\assets\config.properties
echo. >> app\src\main\assets\config.properties

echo [成功] 配置文件已生成
echo   - PC IP: %PC_IP%
echo   - 设备 ID: %DEVICE_ID%
echo.

echo [4/5] 开始构建 APK...
echo.
echo 这可能需要 5-10 分钟（首次构建）...
echo.

REM 清理旧的构建
%GRADLE_CMD% clean >nul 2>&1

REM 构建 APK
%GRADLE_CMD% assembleRelease

if errorlevel 1 (
    echo.
    echo [错误] APK 构建失败
    echo.
    echo 常见问题：
    echo 1. SDK 路径未配置：在项目根目录创建 local.properties 文件
    echo    内容：sdk.dir=C:\\Users\\YourUser\\AppData\\Local\\Android\\Sdk
    echo.
    echo 2. Gradle 版本不兼容：检查 gradle\wrapper\gradle-wrapper.properties
    echo.
    echo 3. 依赖下载失败：检查网络连接
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] 重命名并复制 APK...
echo.

REM 生成时间戳
for /f "tokens=2 delims==" %%i in ('wmic os get localdatetime /value') do set datetime=%%i
set DATE_STR=%datetime:~0,8%

REM 查找 APK 文件
set APK_SOURCE=app\build\outputs\apk\release\app-release.apk
set APK_TARGET=UFO3_Galaxy_%DEVICE_ID%_%DATE_STR%.apk

if not exist "%APK_SOURCE%" (
    echo [错误] APK 文件不存在: %APK_SOURCE%
    pause
    exit /b 1
)

REM 复制到当前目录
copy "%APK_SOURCE%" "%APK_TARGET%" >nul

if errorlevel 1 (
    echo [错误] APK 复制失败
    pause
    exit /b 1
)

echo ================================================================================
echo 构建成功！
echo ================================================================================
echo.
echo APK 文件: %APK_TARGET%
echo 设备: %DEVICE_NAME%
echo PC IP: %PC_IP%
echo.
echo 下一步：
echo.
echo 1. 将 APK 传输到您的 %DEVICE_NAME%
echo.
echo 2. 在设备上安装 APK
echo.
echo 3. 打开应用，授予以下权限：
echo    - 无障碍服务权限（必需）
echo    - 悬浮窗权限（必需）
echo    - 存储权限（可选）
echo.
echo 4. 确保 PC 和设备在同一个 Tailscale 网络中
echo.
echo 5. 在 PC 上启动 UFO³ Galaxy 系统：
echo    start_system.bat
echo.
echo 详细说明请参考：ANDROID_QUICK_INSTALL.md
echo.
pause

cd ..\..\..
