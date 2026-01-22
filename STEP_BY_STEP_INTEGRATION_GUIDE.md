# UFO³ Galaxy - 详细集成步骤指南

**从零开始，手把手教您如何将所有代码集成到您的 Windows 电脑上的 UFO³ Galaxy 系统中。**

---

## 📋 前提条件

在开始之前，请确保您已经：
- ✅ 在 E 盘安装了 Microsoft UFO³ 原项目
- ✅ 在 E 盘克隆了 ufo-galaxy 增强项目
- ✅ 安装了 Python 3.9+
- ✅ 安装了 Podman Desktop（用于容器管理）
- ✅ 配置了 Tailscale VPN

---

## 第一步：拉取最新代码

打开 **Windows PowerShell** 或 **命令提示符**：

```powershell
# 进入项目目录
cd E:\ufo-galaxy

# 拉取最新代码
git pull origin master
```

**验证：**
- 应该看到类似 "Already up to date" 或显示下载的文件列表
- 确认以下目录存在：
  - `E:\ufo-galaxy\windows_client\`
  - `E:\ufo-galaxy\galaxy_gateway\`
  - `E:\ufo-galaxy\enhancements\clients\android_client\`

---

## 第二步：安装 Windows Client 依赖

```powershell
# 进入 Windows Client 目录
cd E:\ufo-galaxy\windows_client

# 安装依赖
pip install -r requirements.txt
```

**可能遇到的问题：**

**问题 1：** `pip` 命令找不到
- **解决：** 确保 Python 已添加到系统 PATH
- **或使用：** `python -m pip install -r requirements.txt`

**问题 2：** pywin32 安装失败
- **解决：** 以管理员身份运行 PowerShell，然后重新安装

**验证：**
```powershell
python -c "import PyQt5; print('PyQt5 OK')"
python -c "import comtypes; print('comtypes OK')"
python -c "import win32com.client; print('pywin32 OK')"
```

---

## 第三步：安装 Galaxy Gateway 依赖

```powershell
# 进入 Galaxy Gateway 目录
cd E:\ufo-galaxy\galaxy_gateway

# 安装依赖（如果还没有安装）
pip install fastapi uvicorn websockets requests
```

**验证：**
```powershell
python -c "import fastapi; print('FastAPI OK')"
python -c "import uvicorn; print('Uvicorn OK')"
```

---

## 第四步：配置 Galaxy Gateway

### 4.1 检查配置文件

查看 `E:\ufo-galaxy\galaxy_gateway\main.py`，确认端口设置：

```python
# 应该在文件末尾看到：
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9000,  # Galaxy Gateway 使用 9000 端口
        log_level="info"
    )
```

### 4.2 检查静态文件

确认 `E:\ufo-galaxy\galaxy_gateway\static\dashboard.html` 文件存在。

---

## 第五步：启动 Galaxy Gateway

```powershell
# 进入 Galaxy Gateway 目录
cd E:\ufo-galaxy\galaxy_gateway

# 启动 Galaxy Gateway
python main.py
```

**预期输出：**
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
```

**验证：**
1. 打开浏览器
2. 访问 http://localhost:9000
3. 应该看到 **UFO³ GALAXY - CONTROL CENTER** 的 Dashboard

**如果看不到 Dashboard：**
- 检查 `galaxy_gateway/static/` 目录是否存在
- 检查 `dashboard.html` 文件是否存在
- 查看终端是否有错误信息

**保持这个终端窗口打开，Galaxy Gateway 需要一直运行！**

---

## 第六步：配置 Windows Client

### 6.1 修改配置文件（可选）

如果需要修改 Galaxy Gateway 的地址，编辑 `E:\ufo-galaxy\windows_client\main.py`：

```python
# 找到这一行（大约在第 30 行）
# 如果 Galaxy Gateway 运行在不同的地址，修改这里
GALAXY_GATEWAY_URL = "http://localhost:9000"
```

### 6.2 测试 Windows Client

**打开一个新的 PowerShell 窗口**（保持 Galaxy Gateway 运行）：

```powershell
# 进入 Windows Client 目录
cd E:\ufo-galaxy\windows_client

# 启动 Windows Client
python main.py
```

**预期结果：**
- 应该看到类似 "Windows Client 初始化成功" 的日志
- **按 F12 键**，侧边栏应该从右侧滑入
- 侧边栏显示黑白渐变风格的 UI

**如果侧边栏没有出现：**
- 检查终端是否有错误信息
- 尝试再次按 F12 键
- 确认 PyQt5 已正确安装

---

## 第七步：测试 Windows 自主操纵功能

在 Windows Client 的侧边栏中：

### 测试 1：打开记事本
1. 在输入框中输入：`打开记事本`
2. 按 Enter
3. **预期：** 记事本应用打开

### 测试 2：查看剪贴板
1. 先复制一些文本到剪贴板（Ctrl+C）
2. 在输入框中输入：`剪贴板`
3. 按 Enter
4. **预期：** 侧边栏显示剪贴板内容

### 测试 3：输入文本
1. 打开记事本
2. 在侧边栏输入：`输入 Hello World`
3. 按 Enter
4. **预期：** 记事本中出现 "Hello World"

### 测试 4：获取屏幕状态
1. 在输入框中输入：`屏幕`
2. 按 Enter
3. **预期：** 侧边栏显示当前窗口名称

---

## 第八步：集成到 Microsoft UFO³ 原项目

### 8.1 理解架构

您现在有两个系统：
- **Microsoft UFO³ 原项目**（在 `E:\UFO\`）
- **UFO³ Galaxy 增强项目**（在 `E:\ufo-galaxy\`）

它们的关系是：
- **Galaxy Gateway** 作为超级网关，统一管理所有节点和设备
- **Windows Client** 作为本地客户端，提供 UI 和自主操纵能力
- **Microsoft UFO³** 的 Device Agent 可以通过 Galaxy Gateway 进行增强

### 8.2 配置 Microsoft UFO³ 连接到 Galaxy Gateway

编辑 Microsoft UFO³ 的配置文件（通常是 `config.yaml` 或类似文件）：

```yaml
# 添加 Galaxy Gateway 的地址
galaxy_gateway:
  enabled: true
  url: "http://localhost:9000"
  
# 如果有 WebSocket 配置
websocket:
  url: "ws://localhost:9000/ws/agent"
```

**注意：** 具体的配置文件位置和格式取决于您的 Microsoft UFO³ 版本。

### 8.3 启动 Microsoft UFO³

按照 Microsoft UFO³ 的官方文档启动系统。

---

## 第九步：配置 Android 设备

### 9.1 构建 Android APK

**在 Windows 上：**

1. 确保已安装 Android Studio

2. 打开项目：
   ```
   E:\ufo-galaxy\enhancements\clients\android_client
   ```

3. 修改配置：
   - 打开 `app/src/main/assets/config.properties`
   - 将 `galaxy.gateway.url` 改为您的 Windows PC 的 Tailscale IP
   - 例如：`galaxy.gateway.url=http://100.x.x.x:9000`

4. 构建 APK：
   - 在 Android Studio 中：Build → Build APK(s)
   - 等待构建完成

5. 安装到设备：
   - 将生成的 APK 文件传输到您的手机/平板
   - 安装 APK

### 9.2 配置 Android 设备

1. 打开 UFO³ Galaxy Android App

2. 开启无障碍服务：
   - 进入"设置" → "无障碍" → "UFO³ Galaxy 自主操纵"
   - 开启服务

3. 授予悬浮窗权限：
   - 进入"设置" → "应用" → "UFO³ Galaxy" → "悬浮窗权限"
   - 允许

4. 测试连接：
   - 在 App 中点击"测试连接"
   - 应该显示"连接成功"

---

## 第十步：验证整个系统

### 10.1 检查 Galaxy Gateway Dashboard

1. 访问 http://localhost:9000
2. 检查"连接设备"面板
3. 应该看到：
   - Windows PC（主控节点）
   - 您的 Android 设备（如果已连接）

### 10.2 测试跨设备命令

**从 Windows Client 控制 Android 设备：**
1. 在 Windows Client 侧边栏输入：`在手机上打开微信`
2. 按 Enter
3. **预期：** 您的 Android 设备打开微信

**从 Android 设备控制 Windows PC：**
1. 在 Android App 的悬浮窗输入：`在电脑上打开记事本`
2. 发送
3. **预期：** Windows PC 打开记事本

---

## 常见问题

### Q1: Galaxy Gateway 启动失败

**错误：** `Address already in use`
- **原因：** 9000 端口被占用
- **解决：** 
  1. 找到占用端口的程序：`netstat -ano | findstr :9000`
  2. 关闭该程序，或修改 Galaxy Gateway 的端口

### Q2: Windows Client 侧边栏不显示

**可能原因：**
- PyQt5 未正确安装
- 显示器分辨率问题

**解决：**
1. 重新安装 PyQt5：`pip install --upgrade PyQt5`
2. 检查终端错误信息

### Q3: Android 设备无法连接

**可能原因：**
- Tailscale 未连接
- IP 地址配置错误
- 防火墙阻止

**解决：**
1. 确认 Tailscale 在 Windows 和 Android 上都已连接
2. 在 Android 上 ping Windows 的 Tailscale IP
3. 检查 Windows 防火墙，允许 9000 端口

### Q4: 自主操纵功能不工作

**可能原因：**
- 权限不足
- UI Automation 未正确初始化

**解决：**
1. 以管理员身份运行 Windows Client
2. 检查终端错误信息

---

## 下一步

集成完成后，您可以：
1. 阅读 `SYSTEM_IMPROVEMENT_ANALYSIS.md` 了解还可以增强的功能
2. 根据 `INTEGRATION_TEST_GUIDE.md` 进行更全面的测试
3. 开始使用您的 UFO³ Galaxy 系统！

---

## 需要帮助？

如果遇到问题：
1. 检查所有终端的错误信息
2. 查看 Galaxy Gateway Dashboard 的日志
3. 确认所有服务都在运行
4. 检查网络连接（Tailscale）

---

**文档版本：** 1.0  
**最后更新：** 2026-01-22  
**作者：** Manus AI
