@echo off
REM UFO³ Galaxy - Academic System Startup Script
REM 学术系统启动脚本

echo ========================================
echo UFO³ Galaxy - Academic System
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 未安装
    echo 请访问 https://www.python.org/downloads/ 安装 Python
    pause
    exit /b 1
)

echo [OK] Python 已安装
echo.

REM 设置环境变量
echo [INFO] 配置环境变量...
set NODE_97_PORT=8097
set NODE_104_PORT=8104
set NODE_80_PORT=8080
set MEMOS_URL=http://localhost:5230
echo [OK] 环境变量已配置
echo.

REM 检查 Memos Token
if "%MEMOS_TOKEN%"=="" (
    echo [WARNING] 未配置 MEMOS_TOKEN
    echo 论文笔记将无法自动保存到 Memos
    echo 请设置环境变量: set MEMOS_TOKEN=your_token
    echo.
)

REM 启动核心学术节点
echo ========================================
echo 启动核心学术节点...
echo ========================================
echo.

REM Node 97: 学术搜索
echo [1/3] 启动 Node_97 (学术搜索)...
cd nodes\Node_97_AcademicSearch
start "Node_97_AcademicSearch" cmd /k "python main.py"
timeout /t 3 /nobreak >nul
cd ..\..
echo [OK] Node_97 已启动 (http://localhost:8097)
echo.

REM Node 104: AgentCPM
echo [2/3] 启动 Node_104 (AgentCPM)...
cd nodes\Node_104_AgentCPM
start "Node_104_AgentCPM" cmd /k "python main.py"
timeout /t 3 /nobreak >nul
cd ..\..
echo [OK] Node_104 已启动 (http://localhost:8104)
echo.

REM Node 80: 记忆系统
echo [3/3] 启动 Node_80 (记忆系统)...
cd nodes\Node_80_MemorySystem
start "Node_80_MemorySystem" cmd /k "python main.py"
timeout /t 3 /nobreak >nul
cd ..\..
echo [OK] Node_80 已启动 (http://localhost:8080)
echo.

echo ========================================
echo 所有学术节点已启动！
echo ========================================
echo.
echo 可用服务:
echo - Node_97 (学术搜索): http://localhost:8097
echo - Node_104 (AgentCPM): http://localhost:8104
echo - Node_80 (记忆系统): http://localhost:8080
echo.
echo 快速测试:
echo   curl http://localhost:8097/health
echo   curl http://localhost:8104/health
echo   curl http://localhost:8080/health
echo.
echo 运行完整研究工作流:
echo   python academic_research_workflow.py "量子机器学习"
echo.
echo 按任意键退出...
pause >nul
