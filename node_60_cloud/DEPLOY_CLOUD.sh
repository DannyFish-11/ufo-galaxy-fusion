#!/bin/bash
# UFO³ Galaxy 华为云节点一键部署脚本

set -e  # 遇到错误立即退出

echo "========================================"
echo "   UFO³ Galaxy 华为云节点部署脚本"
echo "========================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为 root 用户
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}[警告] 建议不要以 root 用户运行此脚本${NC}"
    echo "按 Ctrl+C 取消，或按任意键继续..."
    read -n 1 -s
fi

# 步骤 1: 检查 Python 环境
echo "[1/7] 检查 Python 环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}[✓]${NC} Python 已安装: $PYTHON_VERSION"
else
    echo -e "${RED}[错误]${NC} 未检测到 Python 3"
    echo "正在安装 Python 3..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip
fi

# 步骤 2: 检查 pip
echo ""
echo "[2/7] 检查 pip..."
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}[✓]${NC} pip 已安装"
else
    echo "正在安装 pip..."
    sudo apt-get install -y python3-pip
fi

# 步骤 3: 安装系统依赖
echo ""
echo "[3/7] 安装系统依赖..."
sudo apt-get install -y curl wget git
echo -e "${GREEN}[✓]${NC} 系统依赖已安装"

# 步骤 4: 检查 Tailscale
echo ""
echo "[4/7] 检查 Tailscale..."
if command -v tailscale &> /dev/null; then
    echo -e "${GREEN}[✓]${NC} Tailscale 已安装"
    TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "")
    if [ -z "$TAILSCALE_IP" ]; then
        echo -e "${YELLOW}[警告]${NC} Tailscale 未连接，请先运行: sudo tailscale up"
        echo "按任意键继续..."
        read -n 1 -s
    else
        echo -e "${GREEN}[✓]${NC} Tailscale IP: $TAILSCALE_IP"
    fi
else
    echo -e "${YELLOW}[警告]${NC} 未检测到 Tailscale"
    echo "是否现在安装 Tailscale? (y/n)"
    read -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        curl -fsSL https://tailscale.com/install.sh | sh
        echo "请运行: sudo tailscale up"
        echo "然后重新运行此脚本"
        exit 0
    fi
fi

# 步骤 5: 安装 Python 依赖
echo ""
echo "[5/7] 安装 Python 依赖..."
cd "$(dirname "$0")"
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --user
    echo -e "${GREEN}[✓]${NC} Python 依赖已安装"
else
    echo -e "${YELLOW}[警告]${NC} 未找到 requirements.txt"
    echo "手动安装核心依赖..."
    pip3 install websockets requests qiskit qiskit-ibm-runtime --user
fi

# 步骤 6: 配置环境变量
echo ""
echo "[6/7] 配置环境变量..."

# 获取 Windows PC 的 Tailscale IP
echo "请输入 Windows PC 的 Tailscale IP 地址 (例如: 100.123.215.126):"
read -r WINDOWS_IP
if [ -z "$WINDOWS_IP" ]; then
    echo -e "${YELLOW}[警告]${NC} 未输入 IP，使用默认值 100.123.215.126"
    WINDOWS_IP="100.123.215.126"
fi

# 创建环境变量文件
cat > .env << EOF
# UFO³ Galaxy 华为云节点环境变量
TAILSCALE_IP=$WINDOWS_IP
NODE_50_URL=ws://$WINDOWS_IP:8050
DEVICE_ID=Node_60_Cloud_Compute
QUANTUM_PROVIDER=IBM_QUANTUM
IBM_QUANTUM_TOKEN=
ATLAS_MODE=MOCK
EOF

echo -e "${GREEN}[✓]${NC} 环境变量已配置"
echo "如需配置 IBM Quantum Token，请编辑 .env 文件"

# 步骤 7: 创建启动脚本
echo ""
echo "[7/7] 创建启动脚本..."
cat > start_node60.sh << 'EOF'
#!/bin/bash
# 加载环境变量
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

echo "========================================"
echo "   启动 Node 60 - 异构计算节点"
echo "========================================"
echo "连接目标: $NODE_50_URL"
echo ""

# 启动节点
python3 main.py
EOF

chmod +x start_node60.sh
echo -e "${GREEN}[✓]${NC} 启动脚本已创建"

# 完成
echo ""
echo "========================================"
echo "   部署完成！"
echo "========================================"
echo ""
echo "启动 Node 60:"
echo "  ./start_node60.sh"
echo ""
echo "或者使用 systemd 服务（开机自启）:"
echo "  sudo cp node60.service /etc/systemd/system/"
echo "  sudo systemctl enable node60"
echo "  sudo systemctl start node60"
echo ""
