# UFO³ Galaxy 安卓端快速安装指南

**预计时间**: 15-20 分钟  
**难度**: ⭐⭐

---

## 第一步：获取 PC 的 Tailscale IP (2 分钟)

在您的华为 MateBook 上打开命令行（CMD 或 PowerShell），运行：

```bash
tailscale status
```

找到您的 PC 的 IP 地址（格式：`100.x.x.x`），**记下来**。

---

## 第二步：打包 APK (10 分钟)

### 在 Windows 上

1. 打开命令行，进入项目目录：
   ```bash
   cd ufo-galaxy\enhancements\clients\android_client
   ```

2. 运行打包脚本：
   ```bash
   build_configured_apk.bat
   ```

3. 按提示输入：
   - **PC 的 Tailscale IP**: 输入第一步记下的 IP
   - **设备 ID**: 
     - 小米 14 输入：`xiaomi-14`
     - OPPO 平板输入：`oppo-tablet`

4. 等待构建完成（首次构建需要 5-10 分钟）

5. 构建成功后，您会在当前目录下看到：
   - `UFO3_Galaxy_xiaomi-14_20260122.apk`

6. **为第二台设备重复步骤 2-5**，使用不同的设备 ID。

---

## 第三步：安装 APK (3 分钟)

### 方法 A：通过 ADB 安装（推荐）

1. 用 USB 连接安卓设备到 PC
2. 在命令行中运行：
   ```bash
   # 检查设备是否连接
   adb devices
   
   # 安装 APK（将文件名替换为实际的 APK 文件名）
   adb install -r UFO3_Galaxy_xiaomi-14_20260122.apk
   ```

### 方法 B：手动传输安装

1. 将 APK 文件通过微信/QQ/邮件发送到安卓设备
2. 在设备上下载并点击 APK 文件
3. 允许安装来自未知来源的应用
4. 点击"安装"

---

## 第四步：授予权限 (5 分钟)

### 必需权限（非常重要！）

1. **无障碍服务** ⭐⭐⭐⭐⭐
   - 打开 `设置` -> `无障碍` -> `已安装的应用`
   - 找到 `UFO³ Galaxy` 并**开启服务**
   - **这是最重要的权限！**

2. **显示在其他应用上层**
   - 打开 `设置` -> `应用管理` -> `UFO³ Galaxy` -> `权限管理`
   - 开启"显示在其他应用上层"

3. **屏幕录制**（首次使用时授权）
   - 当 PC 请求屏幕数据时，会弹出授权提示
   - 点击"立即开始"

---

## 第五步：验证连接 (2 分钟)

1. 确保 PC 端的 UFO³ Galaxy 系统正在运行：
   ```bash
   cd ufo-galaxy
   start_ufo3_galaxy.bat
   ```

2. 确保安卓设备和 PC 都已连接到 Tailscale

3. 打开安卓设备上的 `UFO³ Galaxy` 应用

4. 如果看到"已连接到网关"或绿色状态指示，说明连接成功！

---

## 常见问题

**Q: 构建时提示 "SDK location not found"?**

A: 在 `enhancements/clients/android_client` 目录下创建 `local.properties` 文件，内容：
```
sdk.dir=C:\\Users\\YourUser\\AppData\\Local\\Android\\Sdk
```
（将路径替换为您的 Android SDK 实际路径）

**Q: 应用闪退？**

A: 检查**无障碍服务**权限是否已开启。

**Q: 应用显示"连接失败"？**

A: 检查：
1. PC 的 Tailscale IP 是否正确
2. PC 和安卓设备是否在同一个 Tailscale 网络中
3. PC 端的 UFO³ Galaxy 是否正在运行

**Q: 如何为第二台设备打包？**

A: 重新运行 `build_configured_apk.bat`，输入不同的设备 ID（例如 `oppo-tablet`）。

---

## 小米 14 特殊说明

### 开启开发者模式
1. `设置` -> `我的设备` -> `全部参数`
2. 连续点击 `MIUI 版本` 7 次
3. 返回 `设置` -> `更多设置` -> `开发者选项`
4. 开启 `USB 调试` 和 `USB 调试（安全设置）`

### 授权 USB 调试
- 首次连接 PC 时，设备会弹出"允许 USB 调试"提示
- 勾选"始终允许"并点击"允许"

---

## OPPO 平板特殊说明

### 开启开发者模式
1. `设置` -> `关于平板电脑` -> `版本信息`
2. 连续点击 `版本号` 7 次
3. 返回 `设置` -> `其他设置` -> `开发者选项`
4. 开启 `USB 调试`

---

## 完成！

现在您可以在 PC 上通过自然语言控制您的安卓设备了。试试以下命令：

- "截图小米 14 的屏幕"
- "在 OPPO 平板上打开微信"
- "将小米 14 的照片传输到 PC"

祝您使用愉快！🎉
