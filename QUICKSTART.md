# UFO³ Galaxy 快速开始指南

**适用设备**: 华为 MateBook + 小米 14 + OPPO 平板  
**预计时间**: 30-60 分钟  
**难度**: ⭐⭐⭐

---

## 第一步：环境检查 (5 分钟)

在您的华为 MateBook 上打开命令行（CMD 或 PowerShell），进入项目目录并运行环境检查脚本：

```bash
cd ufo-galaxy
python check_environment.py
```

这个脚本会自动检查：
- Python 版本
- ADB 工具
- Git
- Tailscale
- 必需的 Python 包
- 项目结构

如果所有检查都通过，您会看到 `🎉 所有检查通过！` 的提示。

### 常见问题解决

**如果提示 Python 包缺失**:
```bash
pip install -r galaxy_gateway/requirements.txt
```

**如果提示 ADB 未安装**:
- 下载 Android Platform Tools: https://developer.android.com/studio/releases/platform-tools
- 解压后将路径添加到系统环境变量 `Path` 中

**如果提示 Tailscale 未运行**:
- 下载并安装 Tailscale: https://tailscale.com/download/windows
- 安装后使用 Google/Microsoft/GitHub 账号登录

---

## 第二步：配置 Tailscale (10 分钟)

Tailscale 是一个零配置的 VPN，用于让您的 PC、手机和平板在同一个虚拟网络中通信。

### PC 端配置

1. 打开 Tailscale 应用
2. 登录（如果还未登录）
3. 记下您的 PC 的 Tailscale IP 地址（格式：`100.x.x.x`）

在命令行中运行以下命令查看：
```bash
tailscale status
```

### 安卓端配置

在小米 14 和 OPPO 平板上：

1. 打开 Google Play 或应用商店，搜索并安装 `Tailscale`
2. 打开 Tailscale 应用
3. 使用**与 PC 端相同的账号**登录
4. 确保连接状态为"已连接"

现在，您的三台设备应该都在同一个 Tailscale 网络中了。

---

## 第三步：连接安卓设备 (5 分钟)

### 开启 USB 调试

**小米 14**:
1. `设置` -> `我的设备` -> `全部参数`
2. 连续点击 `MIUI 版本` 7 次
3. 返回 `设置` -> `更多设置` -> `开发者选项`
4. 开启 `USB 调试` 和 `USB 调试（安全设置）`

**OPPO 平板**:
1. `设置` -> `关于平板电脑` -> `版本信息`
2. 连续点击 `版本号` 7 次
3. 返回 `设置` -> `其他设置` -> `开发者选项`
4. 开启 `USB 调试`

### 连接并授权

1. 使用 USB 线将设备连接到 PC
2. 在设备上会弹出"允许 USB 调试"的提示，点击**允许**
3. 在 PC 命令行中运行 `adb devices`，确认设备已连接

---

## 第四步：启动系统 (5 分钟)

### 方式一：使用一键启动脚本（推荐）

双击运行 `start_ufo3_galaxy.bat`，脚本会自动：
- 检查环境
- 加载配置
- 启动所有核心节点和扩展节点

### 方式二：手动启动

在命令行中运行：
```bash
python galaxy_launcher.py --include-groups core extended
```

启动过程可能需要 1-2 分钟，请耐心等待。当您看到类似以下的输出时，说明系统已成功启动：

```
[Node 00] StateMachine started on port 8000
[Node 01] OneAPI started on port 8001
[Node 33] ADB started on port 8033
[Node 96] SmartTransportRouter started on port 8096
...
```

---

## 第五步：验证系统 (10 分钟)

运行端到端测试脚本：

```bash
python test_e2e.py
```

这个脚本会自动测试：
- 核心节点健康状态
- 智能传输路由
- ADB 设备连接
- ADB 截图功能
- 量子计算功能（可选）

如果看到 `🎉 所有测试通过！` 或 `⚠️ 大部分测试通过`，说明系统已经可以使用了。

---

## 第六步：安装安卓客户端 (10 分钟)

### 构建 APK

在 PC 的命令行中：

```bash
cd enhancements/clients/android_client
gradlew.bat assembleDebug
```

构建完成后，APK 文件位于：
```
app/build/outputs/apk/debug/app-debug.apk
```

### 安装到设备

为每台安卓设备执行：

```bash
# 查看连接的设备
adb devices

# 安装 APK（将 <device_id> 替换为实际的设备 ID）
adb -s <device_id> install -r app/build/outputs/apk/debug/app-debug.apk
```

### 配置客户端

在每台安卓设备上：

1. 打开 `UFO³ Galaxy` 应用
2. 进入设置
3. 在 `Gateway IP` 字段中填入您的 PC 的 **Tailscale IP 地址**（在第二步中记下的）
4. 保存并重启应用

---

## 第七步：开始使用 (5 分钟)

现在您可以开始使用 UFO³ Galaxy 了！

### 测试跨设备截图

在 PC 的命令行中运行：

```bash
curl -X POST http://localhost:8096/route \
  -H "Content-Type: application/json" \
  -d "{\"device_id\":\"your_phone_id\",\"task_type\":\"static\",\"quality\":\"high\",\"realtime\":false}"
```

将 `your_phone_id` 替换为您在 `adb devices` 中看到的设备 ID。

如果一切正常，系统会自动选择最佳的传输方式（WebRTC/Scrcpy/ADB）来捕获屏幕。

### 测试量子计算

```bash
curl -X POST http://localhost:8051/dispatch \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"Find the shortest path for 5 cities\",\"problem_type\":\"optimization\",\"max_qubits\":10,\"shots\":1024}"
```

系统会自动将自然语言问题转换为量子电路，并推荐最合适的量子算法。

---

## 常见问题

**Q: 启动时报错 "Address already in use"?**  
A: 端口被占用。使用 `netstat -ano | findstr <port>` 找到占用端口的进程并结束它。

**Q: `adb devices` 看不到设备?**  
A: 检查 USB 连接、USB 调试是否开启、驱动是否安装。

**Q: 安卓应用无法连接到 PC?**  
A: 确认：
1. PC 和安卓设备都在 Tailscale 网络中
2. 应用中填写的是 PC 的 Tailscale IP
3. PC 防火墙没有阻止 Tailscale 网络

**Q: 量子计算节点启动失败?**  
A: 安装 Qiskit: `pip install qiskit qiskit-aer qiskit-ibm-runtime`

---

## 下一步

- 阅读完整的部署指南: `DEPLOYMENT_GUIDE_UFO3_GALAXY.md`
- 查看协议融合地图: `PROTOCOL_FUSION_MAP.md`
- 查看量子计算功能: `QUANTUM_FEATURES_VERIFICATION.md`
- 探索更多节点: `nodes/` 目录

---

**祝您使用愉快！**

如有问题，请查看 GitHub Issues 或联系开发者。
