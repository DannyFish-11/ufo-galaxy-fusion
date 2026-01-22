@echo off
REM 启动 Node_105 (Unified Knowledge Base) 和 Node_106 (GitHub Flow)
REM 作者：Manus AI
REM 日期：2026-01-22

echo ================================================================================
echo 启动 UFO3 Galaxy - 知识库和 GitHub 工作流节点
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

echo [1/4] 检查依赖...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo [警告] fastapi 未安装，正在安装...
    pip install fastapi uvicorn httpx pydantic
)

echo.
echo [2/4] 启动 Node_105 (Unified Knowledge Base)...
echo 端口: 8105
echo.
start "Node_105_UnifiedKnowledgeBase" cmd /k "cd nodes\Node_105_UnifiedKnowledgeBase && python main.py"

REM 等待 2 秒
timeout /t 2 /nobreak >nul

echo.
echo [3/4] 启动 Node_106 (GitHub Flow)...
echo 端口: 8106
echo.
start "Node_106_GitHubFlow" cmd /k "cd nodes\Node_106_GitHubFlow && python main.py"

REM 等待 2 秒
timeout /t 2 /nobreak >nul

echo.
echo [4/4] 验证节点状态...
timeout /t 3 /nobreak >nul

curl -s http://localhost:8105/health >nul 2>&1
if errorlevel 1 (
    echo [警告] Node_105 可能未成功启动
) else (
    echo [成功] Node_105 运行中 (http://localhost:8105)
)

curl -s http://localhost:8106/health >nul 2>&1
if errorlevel 1 (
    echo [警告] Node_106 可能未成功启动
) else (
    echo [成功] Node_106 运行中 (http://localhost:8106)
)

echo.
echo ================================================================================
echo 节点已启动！
echo ================================================================================
echo.
echo Node_105 (Unified Knowledge Base):
echo   - URL: http://localhost:8105
echo   - 健康检查: http://localhost:8105/health
echo   - 统计信息: http://localhost:8105/stats
echo.
echo Node_106 (GitHub Flow):
echo   - URL: http://localhost:8106
echo   - 健康检查: http://localhost:8106/health
echo.
echo 运行集成测试:
echo   python test_knowledge_github_integration.py
echo.
echo 按任意键退出...
pause >nul
