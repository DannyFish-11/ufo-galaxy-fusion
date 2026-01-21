# UFO³ Galaxy 智能启动器使用指南

**版本：** 1.0.0  
**日期：** 2026-01-22

---

## 概述

`galaxy_launcher.py` 是 UFO³ Galaxy 的智能启动器，支持：
- ✅ 按需启动（只启动需要的节点）
- ✅ 分组管理（核心/扩展/可选）
- ✅ 依赖管理（自动启动依赖节点）
- ✅ 健康检查（确保节点正常运行）
- ✅ 优雅停止（正确关闭所有节点）

---

## 节点分组

### Core（核心节点）- 必须启动
```
Node 00: StateMachine      - 状态机
Node 01: OneAPI            - 多模型聚合
Node 02: Tasker            - 任务调度
Node 03: Router            - 路由
Node 05: Auth              - 认证
Node 06: Filesystem        - 文件系统
Node 65: LoggerCentral     - 日志中心
Node 67: HealthMonitor     - 健康监控
Node 79: LocalLLM          - 本地大模型
Node 80: MemorySystem      - 记忆系统
```

### Extended（扩展节点）- 按需启动
```
Node 04: Email             - 邮件
Node 07: Git               - Git 控制
Node 08: Calendar          - 日历
Node 09: Sandbox           - 代码沙箱
Node 11: GitHub            - GitHub 集成
Node 12: Postgres          - PostgreSQL
Node 13: SQLite            - SQLite
Node 15: OCR               - 文字识别
Node 19: EdgeTTS           - 语音合成
Node 22: BraveSearch       - 搜索
Node 23: Time              - 时间
Node 24: Weather           - 天气
... (更多)
```

### Optional（可选节点）- 默认不启动
```
Node 10: Slack             - Slack 集成
Node 14: Elasticsearch     - 搜索引擎
Node 18: DeepL             - 翻译
Node 20: S3                - 对象存储
Node 21: Notion            - Notion 集成
Node 25: GoogleSearch      - Google 搜索
Node 31: MQTT              - 物联网
Node 34: BLE               - 蓝牙
Node 52: Qiskit            - 量子计算
... (更多)
```

---

## 使用方法

### 1. 启动核心节点（推荐）

```bash
python galaxy_launcher.py start --group core
```

**启动节点：**
- Node 00, 01, 02, 03, 05, 06, 65, 67, 79, 80

**启动时间：** ~10 秒  
**内存占用：** ~500MB

---

### 2. 启动核心 + 扩展节点

```bash
python galaxy_launcher.py start --group extended
```

**启动节点：**
- 核心节点 + 所有扩展节点

**启动时间：** ~30 秒  
**内存占用：** ~1.5GB

---

### 3. 启动所有节点

```bash
python galaxy_launcher.py start --group all
```

**启动节点：**
- 所有 75 个节点

**启动时间：** ~60 秒  
**内存占用：** ~4GB

---

### 4. 启动指定节点

```bash
# 只启动 LLM 和记忆系统
python galaxy_launcher.py start --nodes 79 80

# 启动多个节点
python galaxy_launcher.py start --nodes 00 01 02 79 80
```

---

### 5. 查看节点状态

```bash
python galaxy_launcher.py status
```

**输出示例：**
```
📊 Node Status:
ID   Name                      Group      Port   Status    
-----------------------------------------------------------------
00   StateMachine              core       8000   🟢 Healthy
01   OneAPI                    core       8001   🟢 Healthy
02   Tasker                    core       8002   🟢 Healthy
...
79   LocalLLM                  core       8079   🟢 Healthy
80   MemorySystem              core       8080   🟢 Healthy

Total: 10/75 nodes running
```

---

### 6. 停止所有节点

```bash
python galaxy_launcher.py stop
```

或者在启动器运行时按 `Ctrl+C`

---

### 7. 重启节点

```bash
# 重启核心节点
python galaxy_launcher.py restart --group core

# 重启指定节点
python galaxy_launcher.py restart --nodes 79 80
```

---

## 高级选项

### 跳过健康检查（加快启动）

```bash
python galaxy_launcher.py start --group core --no-health-check
```

**注意：** 跳过健康检查可能导致节点启动失败但未被发现

---

## 日志

所有节点的日志保存在 `logs/` 目录：

```bash
logs/
├── node_00.log
├── node_01.log
├── node_79.log
├── node_80.log
...
```

**查看日志：**
```bash
# 实时查看 Node 79 日志
tail -f logs/node_79.log

# 查看所有日志
tail -f logs/*.log
```

---

## 性能对比

| 启动模式 | 节点数 | 启动时间 | 内存占用 | 适用场景 |
|---------|--------|---------|---------|---------|
| **Core** | 10 | ~10s | ~500MB | 日常使用 |
| **Extended** | ~40 | ~30s | ~1.5GB | 开发测试 |
| **All** | 75 | ~60s | ~4GB | 完整功能 |
| **Custom** | 自定义 | 可变 | 可变 | 特定任务 |

---

## 依赖管理

启动器会自动处理节点依赖：

**示例：**
```bash
# 启动 Node 02 (Tasker)
python galaxy_launcher.py start --nodes 02

# 自动启动:
# 1. Node 00 (StateMachine) - Node 02 的依赖
# 2. Node 02 (Tasker)
```

**依赖关系：**
- Node 02 → Node 00
- Node 03 → Node 00
- Node 50 → Node 01
- Node 56 → Node 01
- Node 66 → Node 65

---

## 故障排查

### 1. 节点启动失败

**检查：**
```bash
# 查看日志
cat logs/node_XX.log

# 检查端口占用
netstat -tulpn | grep 80XX

# 手动启动测试
cd nodes/Node_XX_Name
python main.py
```

---

### 2. 健康检查失败

**原因：**
- 节点启动慢（需要更多时间）
- 端口被占用
- 依赖服务未启动（如 Redis, Memos）

**解决：**
```bash
# 跳过健康检查
python galaxy_launcher.py start --no-health-check

# 或者等待更长时间后再检查
python galaxy_launcher.py status
```

---

### 3. 端口冲突

**修改端口：**
编辑 `galaxy_launcher.py` 中的 `NODE_CONFIG`

```python
"79": {"name": "LocalLLM", "group": NodeGroup.CORE, "port": 8079, "deps": []},
# 改为
"79": {"name": "LocalLLM", "group": NodeGroup.CORE, "port": 9079, "deps": []},
```

---

## 最佳实践

### 1. 日常使用

```bash
# 只启动核心节点
python galaxy_launcher.py start --group core

# 按需启动其他节点
python galaxy_launcher.py start --nodes 22 24  # 搜索和天气
```

---

### 2. 开发测试

```bash
# 启动核心 + 扩展节点
python galaxy_launcher.py start --group extended

# 查看状态
python galaxy_launcher.py status

# 查看日志
tail -f logs/*.log
```

---

### 3. 生产部署

```bash
# 使用 systemd 或 supervisor 管理
# 创建服务文件 /etc/systemd/system/ufo-galaxy.service

[Unit]
Description=UFO³ Galaxy
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/ufo-galaxy
ExecStart=/usr/bin/python3 galaxy_launcher.py start --group core
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启动服务
sudo systemctl start ufo-galaxy
sudo systemctl enable ufo-galaxy

# 查看状态
sudo systemctl status ufo-galaxy
```

---

## 与 Podman 集成

### 启动容器服务

```powershell
# Windows (Podman Desktop)
podman run -d --name redis -p 6379:6379 redis:alpine
podman run -d --name memos -p 5230:5230 -v E:\ufo-galaxy\data\memos:/var/opt/memos neosmemo/memos:stable
```

### 启动 Galaxy

```bash
# 确保容器服务运行后再启动
python galaxy_launcher.py start --group core
```

---

## 更新日志

### v1.0.0 (2026-01-22)
- ✅ 初始版本
- ✅ 支持按需启动
- ✅ 支持分组管理
- ✅ 支持依赖管理
- ✅ 支持健康检查
- ✅ 支持优雅停止

---

## 相关链接

- [Node 79 (Local LLM)](nodes/Node_79_LocalLLM/README.md)
- [Node 80 (Memory System)](nodes/Node_80_MemorySystem/README.md)
- [节点精简计划](NODE_CLEANUP_PLAN.md)
- [废弃节点列表](DEPRECATED_NODES.md)
