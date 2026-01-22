@echo off
REM UFO³ Galaxy - Optimized Startup Script
REM 优化版系统启动脚本

echo ========================================
echo UFO³ Galaxy - Optimized Startup
echo ========================================
echo.

REM 检查环境
echo [INFO] 检查环境...
python check_environment.py
if errorlevel 1 (
    echo [ERROR] 环境检查失败
    echo 请先运行: python check_environment.py
    pause
    exit /b 1
)
echo [OK] 环境检查通过
echo.

REM 配置选择
echo 请选择启动模式:
echo 1. 完整系统 (所有节点)
echo 2. 学术系统 (Node_97 + Node_104 + Node_80)
echo 3. 核心系统 (Gateway + 基础节点)
echo 4. 最小系统 (仅 Gateway)
echo.
set /p MODE="请输入选择 (1-4): "

if "%MODE%"=="1" goto FULL_SYSTEM
if "%MODE%"=="2" goto ACADEMIC_SYSTEM
if "%MODE%"=="3" goto CORE_SYSTEM
if "%MODE%"=="4" goto MINIMAL_SYSTEM

echo [ERROR] 无效选择
pause
exit /b 1

:FULL_SYSTEM
echo.
echo ========================================
echo 启动完整系统...
echo ========================================
echo.
call start_ufo3_galaxy.bat
goto END

:ACADEMIC_SYSTEM
echo.
echo ========================================
echo 启动学术系统...
echo ========================================
echo.
call start_academic_system.bat
goto END

:CORE_SYSTEM
echo.
echo ========================================
echo 启动核心系统...
echo ========================================
echo.

REM 启动 Gateway
echo [1/5] 启动 Galaxy Gateway...
cd galaxy_gateway
start "GalaxyGateway" cmd /k "python gateway_service_v3.py"
timeout /t 5 /nobreak >nul
cd ..
echo [OK] Gateway 已启动 (http://localhost:8000)
echo.

REM 启动核心节点
echo [2/5] 启动 Node_79 (Local LLM)...
cd nodes\Node_79_LocalLLM
start "Node_79" cmd /k "python main.py"
timeout /t 3 /nobreak >nul
cd ..\..
echo [OK] Node_79 已启动
echo.

echo [3/5] 启动 Node_80 (Memory System)...
cd nodes\Node_80_MemorySystem
start "Node_80" cmd /k "python main.py"
timeout /t 3 /nobreak >nul
cd ..\..
echo [OK] Node_80 已启动
echo.

echo [4/5] 启动 Node_81 (Orchestrator)...
cd nodes\Node_81_Orchestrator
start "Node_81" cmd /k "python main.py"
timeout /t 3 /nobreak >nul
cd ..\..
echo [OK] Node_81 已启动
echo.

echo [5/5] 启动 Node_96 (Smart Transport Router)...
cd nodes\Node_96_SmartTransportRouter
start "Node_96" cmd /k "python main.py"
timeout /t 3 /nobreak >nul
cd ..\..
echo [OK] Node_96 已启动
echo.

echo ========================================
echo 核心系统已启动！
echo ========================================
goto END

:MINIMAL_SYSTEM
echo.
echo ========================================
echo 启动最小系统...
echo ========================================
echo.

echo [1/1] 启动 Galaxy Gateway...
cd galaxy_gateway
start "GalaxyGateway" cmd /k "python gateway_service_v3.py"
timeout /t 5 /nobreak >nul
cd ..
echo [OK] Gateway 已启动 (http://localhost:8000)
echo.

echo ========================================
echo 最小系统已启动！
echo ========================================
goto END

:END
echo.
echo 系统启动完成！
echo.
echo 运行测试:
echo   python test_e2e.py
echo.
echo 按任意键退出...
pause >nul
