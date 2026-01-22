# UFO³ Galaxy 最终部署清单

**版本**: 1.0  
**日期**: 2026-01-22  
**目标**: 30-60 分钟内完成所有设备的部署，并成功运行您的第一个跨设备指令。

---

## 🚀 第一部分：PC 端环境准备 (华为 MateBook)

**预计时间**: 15 分钟

- [ ] **安装 Python 3.11**: 
  - 访问 [python.org](https://www.python.org/downloads/release/python-3110/)
  - **重要**: 安装时务必勾选 `Add Python to PATH`。

- [ ] **安装 Git**: 
  - 访问 [git-scm.com](https://git-scm.com/download/win)

- [ ] **安装 ADB (安卓调试桥)**: 
  - 访问 [developer.android.com](https://developer.android.com/studio/releases/platform-tools)
  - 下载后，将 `platform-tools` 目录的路径添加到系统的 `Path` 环境变量中。

- [ ] **安装 Tailscale**: 
  - 访问 [tailscale.com/download/windows](https://tailscale.com/download/windows)
  - 安装后，使用您的 Google/Microsoft/GitHub 账号登录。

- [ ] **克隆代码仓库**: 
  - 打开命令行 (CMD 或 PowerShell)，运行：
    ```bash
    git clone https://github.com/DannyFish-11/ufo-galaxy.git
    cd ufo-galaxy
    ```

- [ ] **运行环境检查**: 
  - 在 `ufo-galaxy` 目录下运行：
    ```bash
    python check_environment.py
    ```
  - 根据提示安装缺失的 Python 包（例如 `pip install -r galaxy_gateway/requirements.txt`）。

---

## 🌐 第二部分：网络配置 (所有设备)

**预计时间**: 5 分钟

- [ ] **登录 Tailscale**: 
  - 在**小米 14** 和 **OPPO 平板**的应用商店中下载并安装 `Tailscale`。
  - 确保您的 PC、小米 14、OPPO 平板都使用**同一个账号**登录 Tailscale。

- [ ] **验证网络连通**: 
  - 在 PC 命令行中运行 `tailscale status`。
  - 您应该能看到您的三台设备都在列表中。

- [ ] **记录 PC IP 地址**: 
  - 在 `tailscale status` 的输出中，找到您的 PC 的 IP 地址（格式为 `100.x.x.x`），并**记下来**。

---

## 📱 第三部分：安卓设备准备 (小米 14 & OPPO 平板)

**预计时间**: 10 分钟

- [ ] **开启开发者模式**: 
  - **小米 14**: `设置` -> `我的设备` -> `全部参数` -> 连续点击 `MIUI 版本` 7 次。
  - **OPPO 平板**: `设置` -> `关于平板电脑` -> `版本信息` -> 连续点击 `版本号` 7 次。

- [ ] **开启 USB 调试**: 
  - **小米 14**: `设置` -> `更多设置` -> `开发者选项` -> 开启 `USB 调试` 和 `USB 调试（安全设置）`。
  - **OPPO 平板**: `设置` -> `其他设置` -> `开发者选项` -> 开启 `USB 调试`。

- [ ] **连接并授权**: 
  - 使用 USB 线将设备连接到 PC。
  - 在设备上会弹出“允许 USB 调试”的提示，勾选“始终允许”并点击**允许**。
  - 在 PC 命令行中运行 `adb devices`，确认设备已连接。

---

## 📦 第四部分：打包并安装安卓客户端 (PC)

**预计时间**: 15 分钟

- [ ] **为小米 14 打包**: 
  - 在 PC 命令行中，进入目录 `ufo-galaxy\enhancements\clients\android_client`。
  - 运行 `build_configured_apk.bat`。
  - 按提示输入：
    - **PC 的 Tailscale IP**: 您在第二部分记下的 IP。
    - **设备 ID**: `xiaomi-14`
  - 等待构建完成（首次构建需要 5-10 分钟）。

- [ ] **为 OPPO 平板打包**: 
  - 再次运行 `build_configured_apk.bat`。
  - 按提示输入：
    - **PC 的 Tailscale IP**: 相同的 IP。
    - **设备 ID**: `oppo-tablet`

- [ ] **安装 APK 到小米 14**: 
  - 在 PC 命令行中运行：
    ```bash
    adb -s <小米14的设备ID> install -r UFO3_Galaxy_xiaomi-14_*.apk
    ```
    (将 `<小米14的设备ID>` 替换为 `adb devices` 中显示的 ID)

- [ ] **安装 APK 到 OPPO 平板**: 
  - 在 PC 命令行中运行：
    ```bash
    adb -s <OPPO平板的设备ID> install -r UFO3_Galaxy_oppo-tablet_*.apk
    ```

---

## 🚀 第五部分：启动系统 (PC)

**预计时间**: 2 分钟

- [ ] **运行一键启动脚本**: 
  - 在 `ufo-galaxy` 根目录下，双击运行 `start_ufo3_galaxy.bat`。
  - 等待所有核心节点启动完成。

---

## ✅ 第六部分：最终验证

**预计时间**: 5 分钟

- [ ] **PC 端测试**: 
  - 打开一个新的命令行窗口，进入 `ufo-galaxy` 目录。
  - 运行 `python test_e2e.py`。
  - 确认看到 `🎉 所有测试通过！` 或 `⚠️ 大部分测试通过`。

- [ ] **安卓端权限配置**: 
  - 在小米 14 和 OPPO 平板上，打开新安装的 `UFO³ Galaxy` 应用。
  - 根据提示，或手动进入设置，开启**最重要的两个权限**：
    - **无障碍服务**: `设置` -> `无障碍` -> `已安装的应用` -> `UFO³ Galaxy` -> **开启**。
    - **显示在其他应用上层**: `设置` -> `应用管理` -> `UFO³ Galaxy` -> `权限管理` -> **开启**。

- [ ] **安卓端连接验证**: 
  - 重新打开 `UFO³ Galaxy` 应用。
  - 确认应用界面显示“已连接到网关”或绿色状态指示。

---

## 🎉 恭喜！部署完成！

您已经成功部署了 UFO³ Galaxy 系统！现在，您可以开始体验它的强大功能了。

**下一步**: 查看 `FIRST_USE_GUIDE.md`，尝试您的第一个跨设备指令！
