# UFO Galaxy 与 UFO3 集成指南

本文档说明如何将 UFO Galaxy 64核系统集成到您的 UFO3 环境中。

## 快速安装

```bash
# 解压到任意位置
tar -xzf ufo-galaxy-podman.tar.gz
cd ufo-galaxy-podman

# 一键安装到 /opt/ufo-galaxy
sudo ./install.sh

# 或安装到自定义位置
./install.sh ~/ufo-galaxy
```

## 目录结构

安装后的目录结构：

```
/opt/ufo-galaxy/              # 或您指定的安装目录
├── bootstrap.sh              # 主控脚本
├── install.sh                # 安装脚本
├── podman-compose.yml        # 容器编排
├── config/
│   ├── .env                  # 环境变量配置
│   └── whitelist.json        # 安全白名单
├── nodes/                    # 所有节点代码
│   ├── Node_00_StateMachine/
│   ├── Node_50_Transformer/
│   ├── Node_58_ModelRouter/
│   └── ...
├── scripts/
│   └── launcher_v2.py
├── tests/
├── data/                     # 运行时数据
├── logs/                     # 日志目录
└── backups/                  # 备份目录
```

## 配置

### 必要配置

编辑 `config/.env`：

```bash
# API 密钥 (根据需要配置)
OPENAI_API_KEY=sk-your-key
ANTHROPIC_API_KEY=sk-ant-your-key

# 本地模型 (如果使用 Ollama)
OLLAMA_URL=http://localhost:11434

# 日志级别
LOG_LEVEL=INFO
```

### 硬件配置

如果您有 Android 设备或 3D 打印机：

```bash
# Android ADB
# 确保设备已连接并授权

# OctoPrint 3D 打印机
OCTOPRINT_URL=http://your-octoprint-ip:5000
OCTOPRINT_API_KEY=your-api-key
```

## 启动方式

### 方式一：直接启动

```bash
cd /opt/ufo-galaxy
./bootstrap.sh start
```

### 方式二：Systemd 服务

```bash
# 启动服务
sudo systemctl start ufo-galaxy

# 开机自启
sudo systemctl enable ufo-galaxy

# 查看状态
sudo systemctl status ufo-galaxy

# 查看日志
sudo journalctl -u ufo-galaxy -f
```

### 方式三：命令行工具

如果安装时创建了 symlink：

```bash
ufo-galaxy start
ufo-galaxy status
ufo-galaxy stop
```

## 端口映射

| 服务 | 端口 | 说明 |
|------|------|------|
| State Machine | 8000 | 全局状态机 |
| Transformer | 8050 | 硬件仲裁器 |
| Model Router | 8058 | 模型路由器 |
| Quantum Dispatcher | 8051 | 量子调度器 |
| Qiskit Simulator | 8052 | 量子模拟器 |
| Symbolic Math | 8054 | 符号数学 |
| Agent Swarm | 8056 | 多智能体 |
| Telemetry | 8064 | 遥测监控 |
| Logger | 8065 | 审计日志 |
| Health Monitor | 8067 | 健康监控 |
| Backup | 8069 | 备份恢复 |
| Dashboard | 8080 | 监控面板 |

## 与现有 UFO3 服务集成

### 网络配置

UFO Galaxy 使用独立的网络命名空间：

- `net_kernel`: 10.88.0.0/24
- `net_gateway`: 10.88.1.0/24
- `net_tools`: 10.88.2.0/24
- `net_phys`: 10.88.3.0/24 (隔离)

如果您的 UFO3 使用不同的网段，可以在 `podman-compose.yml` 中修改。

### 共享 Redis

如果 UFO3 已有 Redis 实例，可以修改 Node 00 使用现有 Redis：

```yaml
# podman-compose.yml
services:
  node_00_statemachine:
    environment:
      - REDIS_URL=redis://your-existing-redis:6379
```

### API 集成

所有节点都提供 REST API，可以从 UFO3 的其他服务调用：

```python
import httpx

# 调用模型路由器
response = httpx.post("http://localhost:8058/route", json={
    "query": "分析这段代码的复杂度",
    "session_id": "ufo3-session-1"
})

# 调用状态机
response = httpx.post("http://localhost:8000/state/set", json={
    "key": "ufo3.task.current",
    "value": {"task_id": "123", "status": "running"}
})
```

## 健康检查

### 手动检查

```bash
./bootstrap.sh status
```

### 程序化检查

```python
import httpx

nodes = [
    ("State Machine", "http://localhost:8000/health"),
    ("Transformer", "http://localhost:8050/health"),
    ("Model Router", "http://localhost:8058/health"),
]

for name, url in nodes:
    try:
        r = httpx.get(url, timeout=5)
        print(f"✅ {name}: {r.status_code}")
    except:
        print(f"❌ {name}: unreachable")
```

## 故障排除

### 容器无法启动

```bash
# 查看日志
podman-compose logs node_00_statemachine

# 检查网络
podman network ls

# 重建镜像
podman-compose build --no-cache
```

### 端口冲突

如果端口已被占用，修改 `podman-compose.yml` 中的端口映射：

```yaml
ports:
  - "18000:8000"  # 改为 18000
```

### Redis 连接失败

```bash
# 检查 Redis 状态
podman exec ufo_redis redis-cli ping

# 查看 Redis 日志
podman logs ufo_redis
```

## 升级

```bash
# 停止服务
./bootstrap.sh stop

# 备份配置
cp -r config config.bak

# 解压新版本
tar -xzf ufo-galaxy-podman-new.tar.gz

# 恢复配置
cp -r config.bak/* config/

# 重建并启动
podman-compose build
./bootstrap.sh start
```

## 卸载

```bash
# 停止服务
./bootstrap.sh stop

# 删除容器和镜像
podman-compose down --rmi all

# 删除数据卷 (可选，会丢失数据)
podman volume rm ufo-galaxy_redis_data ufo-galaxy_telemetry_data ...

# 删除 systemd 服务
sudo rm /etc/systemd/system/ufo-galaxy.service
sudo systemctl daemon-reload

# 删除安装目录
sudo rm -rf /opt/ufo-galaxy
```

## 支持

如有问题，请检查：

1. `./bootstrap.sh status` 输出
2. `podman-compose logs` 日志
3. `tests/` 目录下的测试脚本
