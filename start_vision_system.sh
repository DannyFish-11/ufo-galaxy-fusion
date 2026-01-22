#!/bin/bash

echo "🚀 启动 UFO³ Galaxy 视觉操控系统..."

# 检查环境变量
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ 错误: GEMINI_API_KEY 未设置"
    echo "请运行: export GEMINI_API_KEY='your_api_key'"
    exit 1
fi

# 启动节点
echo "📦 启动 Node_15_OCR..."
cd nodes/Node_15_OCR && python3.11 main_enhanced.py > /tmp/node_15.log 2>&1 &
sleep 2

echo "📦 启动 Node_45_DesktopAuto..."
cd ../Node_45_DesktopAuto && python3.11 main_enhanced.py > /tmp/node_45.log 2>&1 &
sleep 2

echo "📦 启动 Node_90_MultimodalVision..."
cd ../Node_90_MultimodalVision && python3.11 main.py > /tmp/node_90.log 2>&1 &
sleep 2

echo "📦 启动 Node_91_MultimodalAgent..."
cd ../Node_91_MultimodalAgent && python3.11 main.py > /tmp/node_91.log 2>&1 &
sleep 2

echo "📦 启动 Node_92_AutoControl..."
cd ../Node_92_AutoControl && python3.11 main.py > /tmp/node_92.log 2>&1 &
sleep 2

echo "🌐 启动 Galaxy Gateway v4.0..."
cd ../../galaxy_gateway && python3.11 gateway_service_v4.py > /tmp/gateway.log 2>&1 &
sleep 3

echo ""
echo "✅ 所有服务已启动！"
echo ""
echo "📊 健康检查:"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo "📝 日志文件:"
echo "  - Node_15_OCR: /tmp/node_15.log"
echo "  - Node_45_DesktopAuto: /tmp/node_45.log"
echo "  - Node_90_MultimodalVision: /tmp/node_90.log"
echo "  - Node_91_MultimodalAgent: /tmp/node_91.log"
echo "  - Node_92_AutoControl: /tmp/node_92.log"
echo "  - Gateway: /tmp/gateway.log"
echo ""
echo "🎉 视觉操控系统已就绪！"
