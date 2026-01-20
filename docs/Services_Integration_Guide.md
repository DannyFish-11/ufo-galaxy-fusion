# UFO³ Galaxy 第三方服务对接指南

本文档提供所有第三方服务的真实对接方法和配置说明。

## 目录

1. [PixVerse AI 视频生成](#pixverse)
2. [拓竹 Bambu Lab 3D 打印机](#bambu-lab)
3. [51World 数字孪生平台](#51world)
4. [无人机控制](#drone)
5. [OneAPI AI 模型](#oneapi)

---

## 1. PixVerse AI 视频生成 {#pixverse}

### 状态：✅ 真实可用

### 官方文档
- API 文档：https://docs.platform.pixverse.ai/
- 平台地址：https://platform.pixverse.ai/

### 获取 API Key

1. 访问 https://platform.pixverse.ai/
2. 注册账号并登录
3. 进入"API Keys"页面
4. 创建新的 API Key

### 配置方法

编辑 `config/services_config.json`：

```json
{
  "pixverse": {
    "api_key": "YOUR_API_KEY",
    "api_base": "https://app-api.pixverse.ai"
  }
}
```

或设置环境变量：

```bash
export PIXVERSE_API_KEY="YOUR_API_KEY"
```

### 使用示例

```python
from nodes.Node_71_MediaGen.pixverse_adapter import PixVerseAdapter

adapter = PixVerseAdapter()

# 文本生成视频
result = adapter.generate_video(
    prompt="A cat playing piano in a cozy room",
    duration=5,
    quality="540p"
)

print(f"视频 URL: {result['video_url']}")
print(f"本地路径: {result['local_path']}")
```

### 注意事项

- 每次请求必须包含唯一的 `ai-trace-id`（已自动生成）
- 视频生成需要等待时间（通常 1-5 分钟）
- 免费账号有请求限制

---

## 2. 拓竹 Bambu Lab 3D 打印机 {#bambu-lab}

### 状态：✅ 真实可用

### 官方文档
- 官方 Wiki：https://wiki.bambulab.com/en/software/third-party-integration
- 社区文档：https://github.com/Doridian/OpenBambuAPI

### 连接方式

拓竹打印机支持两种连接方式：

#### 方式 1：本地 MQTT（推荐）

**优点**：无需云端，速度快，更稳定

**配置**：

```json
{
  "bambu_lab": {
    "printer_ip": "192.168.1.100",
    "access_code": "12345678",
    "use_cloud": false
  }
}
```

**获取访问码**：
1. 在打印机屏幕上进入"设置"
2. 找到"网络"或"连接"选项
3. 查看"访问码"（Access Code）

#### 方式 2：云端 MQTT

**优点**：可远程访问

**配置**：

```json
{
  "bambu_lab": {
    "serial_number": "01P00A123456789",
    "access_code": "12345678",
    "use_cloud": true
  }
}
```

### 使用示例

```python
from nodes.Node_70_BambuLab.enhanced_bambu_controller import EnhancedBambuController

controller = EnhancedBambuController(
    ip="192.168.1.100",
    port=8883,
    serial="01P00A123456789",
    access_code="12345678"
)

# 获取状态
status = controller.get_human_readable_status()
print(status)

# 获取温度报告
temp_report = controller.get_temperature_report()
print(temp_report)
```

### 注意事项

- 本地连接需要打印机和电脑在同一局域网
- 访问码每次打印机重启可能会变化
- 官方 Cloud API 最近有访问限制

---

## 3. 51World 数字孪生平台 {#51world}

### 状态：⚠️ 需要适配

### 官方文档
- WdpApi 文档：https://wdpapi.51aes.com/
- 平台地址：https://www.51aes.com/

### 重要说明

51World 使用 **JavaScript SDK**，而非 REST API。因此需要以下三种方式之一进行集成：

#### 方式 1：演示模式（当前实现）

**优点**：无需配置，可直接运行

**缺点**：使用本地算法模拟，非真实 51World 数据

**配置**：

```json
{
  "51world": {
    "mode": "demo"
  }
}
```

**使用**：

```python
from nodes.Node_74_DigitalTwin.digital_twin_simulator import DigitalTwinSimulator

simulator = DigitalTwinSimulator(mode="demo")

# 模拟无人机飞行
result = await simulator.simulate_drone_flight(waypoints)
```

#### 方式 2：Node.js 桥接服务（推荐）

**优点**：真实调用 51World SDK

**缺点**：需要额外部署 Node.js 服务

**步骤**：

1. 创建 Node.js 项目：

```bash
mkdir 51world-bridge && cd 51world-bridge
npm init -y
npm install express wdpapi
```

2. 创建桥接服务 `server.js`：

```javascript
const express = require('express');
const WdpApi = require('wdpapi');

const app = express();
app.use(express.json());

// 初始化 51World SDK
const wdp = new WdpApi({
  sceneId: 'YOUR_SCENE_ID'
});

// 模拟无人机飞行
app.post('/simulate/drone', async (req, res) => {
  const { waypoints } = req.body;
  
  // 调用 51World SDK
  const result = await wdp.simulateFlight(waypoints);
  
  res.json(result);
});

app.listen(3000, () => {
  console.log('51World Bridge running on port 3000');
});
```

3. 启动服务：

```bash
node server.js
```

4. 配置 Python 端：

```json
{
  "51world": {
    "mode": "nodejs",
    "nodejs_bridge_url": "http://localhost:3000"
  }
}
```

#### 方式 3：浏览器自动化

**优点**：可直接控制 51World 网页

**缺点**：需要浏览器，速度较慢

**步骤**：

1. 安装 Selenium：

```bash
pip install selenium
```

2. 配置：

```json
{
  "51world": {
    "mode": "browser"
  }
}
```

### 注意事项

- 需要在 51World 平台创建场景并获取 Scene ID
- JavaScript SDK 仅支持浏览器和 Node.js 环境
- 演示模式适用于极客松演示，生产环境建议使用 Node.js 桥接

---

## 4. 无人机控制 {#drone}

### 状态：✅ 真实可用

### 支持的无人机类型

#### 1. MAVLink 协议（通用）

**支持的无人机**：
- PX4
- ArduPilot
- 大部分开源无人机

**配置**：

```json
{
  "drone": {
    "type": "mavlink",
    "connection_string": "udp:127.0.0.1:14550"
  }
}
```

**使用示例**：

```python
from nodes.Node_45_DroneControl.universal_drone_controller import UniversalDroneController

controller = UniversalDroneController(
    drone_type="mavlink",
    connection_string="udp:127.0.0.1:14550"
)

controller.connect()
controller.arm()
controller.takeoff(altitude=10)
```

#### 2. DJI Tello

**优点**：价格便宜，易于开发

**配置**：

```json
{
  "drone": {
    "type": "dji_tello"
  }
}
```

**使用示例**：

```python
controller = UniversalDroneController(drone_type="dji_tello")

controller.connect()
controller.takeoff()
controller.move_forward(50)
controller.land()
```

#### 3. DJI 高端无人机（需要申请）

**支持的型号**：
- Mavic 系列
- Phantom 系列
- Inspire 系列

**步骤**：
1. 访问 https://developer.dji.com/
2. 注册开发者账号
3. 申请 SDK 访问权限
4. 下载 Mobile SDK 或 Onboard SDK

### 注意事项

- MAVLink 需要无人机支持该协议
- DJI Tello 无需申请，即插即用
- DJI 高端无人机需要开发者账号

---

## 5. OneAPI AI 模型 {#oneapi}

### 状态：✅ 真实可用

### 官方文档
- GitHub：https://github.com/songquanpeng/one-api

### 部署 OneAPI

#### 方式 1：Docker 部署

```bash
docker run -d \
  --name oneapi \
  -p 3000:3000 \
  justsong/one-api:latest
```

#### 方式 2：本地部署

```bash
git clone https://github.com/songquanpeng/one-api.git
cd one-api
go build -o one-api
./one-api
```

### 配置

```json
{
  "oneapi": {
    "base_url": "http://localhost:3000/v1",
    "api_key": "sk-xxxxx",
    "model": "gpt-4"
  }
}
```

### 使用示例

```python
from nodes.Node_50_Transformer.enhanced_nlu_engine import EnhancedNLUEngine

engine = EnhancedNLUEngine(
    oneapi_base="http://localhost:3000/v1",
    oneapi_key="sk-xxxxx"
)

intent = await engine.understand("打开记事本")
print(intent.action)  # "open_app"
print(intent.entities)  # {"app_name": "notepad"}
```

### 注意事项

- OneAPI 支持多种 AI 模型（OpenAI、Claude、Gemini 等）
- 需要先在 OneAPI 管理界面添加渠道和令牌
- 可以设置速率限制和额度控制

---

## 总结

| 服务 | 状态 | 难度 | 推荐方式 |
|:---|:---:|:---:|:---|
| **PixVerse** | ✅ 可用 | ⭐ 简单 | 直接使用 API |
| **拓竹 3D 打印机** | ✅ 可用 | ⭐⭐ 中等 | 本地 MQTT |
| **51World** | ⚠️ 需适配 | ⭐⭐⭐ 复杂 | 演示模式（极客松）<br>Node.js 桥接（生产） |
| **无人机控制** | ✅ 可用 | ⭐⭐ 中等 | DJI Tello（入门）<br>MAVLink（高级） |
| **OneAPI** | ✅ 可用 | ⭐ 简单 | Docker 部署 |

---

## 快速开始

1. 复制配置模板：

```bash
cp config/services_config.example.json config/services_config.json
```

2. 编辑配置文件，填入您的 API Key 和设备信息

3. 运行测试：

```bash
python nodes/Node_71_MediaGen/pixverse_adapter.py
python nodes/Node_74_DigitalTwin/digital_twin_simulator.py
```

4. 启动完整系统：

```bash
podman-compose up -d
```

---

## 获取帮助

如有问题，请查看：
- 各节点的 README.md
- 官方文档链接
- GitHub Issues

祝您使用愉快！🚀
