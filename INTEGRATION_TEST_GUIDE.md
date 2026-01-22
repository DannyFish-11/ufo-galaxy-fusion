# UFO³ Galaxy - 集成测试指南

## 概述

本文档提供 Windows 端自主操纵模块和两个 UI 的集成测试指南。

---

## 测试环境准备

### 1. Windows PC 环境

**必需软件：**
- Python 3.9+
- PyQt5
- comtypes
- pywin32

**安装依赖：**
```bash
cd E:\ufo-galaxy\windows_client
pip install -r requirements.txt
```

### 2. Galaxy Gateway

**启动 Galaxy Gateway：**
```bash
cd E:\ufo-galaxy\galaxy_gateway
python main.py
```

**验证：**
- 访问 http://localhost:9000
- 应该看到 Galaxy Gateway Dashboard

---

## 测试项目

### 测试 1: Windows Client UI

**目标：** 验证侧边栏 UI 能正常显示和交互

**步骤：**
1. 启动 Windows Client
   ```bash
   cd E:\ufo-galaxy\windows_client
   python main.py
   ```

2. 按 F12 键（Fn 键的替代）

3. 验证：
   - ✅ 侧边栏从右侧滑入
   - ✅ UI 显示正常（黑白渐变风格）
   - ✅ 输入框可以输入文字
   - ✅ 按 Enter 可以提交命令

**预期结果：**
- 侧边栏显示流畅
- UI 风格符合极简极客黑白渐变
- 输入和交互正常

---

### 测试 2: Windows 自主操纵

**目标：** 验证 Windows 自主操纵功能

**步骤：**
1. 在侧边栏输入框中输入：`打开记事本`

2. 按 Enter 提交

3. 验证：
   - ✅ 系统显示"正在处理..."
   - ✅ 记事本应用被打开
   - ✅ 侧边栏显示成功消息

**预期结果：**
- 记事本成功打开
- 命令执行流程正常

**其他测试命令：**
- `打开计算器` - 打开计算器应用
- `输入 Hello World` - 在当前焦点窗口输入文本
- `剪贴板` - 查看剪贴板内容
- `屏幕` - 获取当前窗口信息

---

### 测试 3: Galaxy Gateway Dashboard

**目标：** 验证 Dashboard 能正常显示系统状态

**步骤：**
1. 打开浏览器，访问 http://localhost:9000

2. 验证：
   - ✅ Dashboard 显示正常
   - ✅ 系统状态显示"在线"
   - ✅ 显示 79 个活跃节点
   - ✅ 显示 10 个 API 提供商
   - ✅ 日志区域显示系统日志

3. 点击"刷新"按钮

4. 验证：
   - ✅ 设备列表更新
   - ✅ 日志显示"刷新设备列表"

**预期结果：**
- Dashboard 显示正常
- 所有数据正确显示
- 交互功能正常

---

### 测试 4: Windows Client 与 Galaxy Gateway 集成

**目标：** 验证 Windows Client 能与 Galaxy Gateway 通信

**前提：**
- Galaxy Gateway 已启动
- Windows Client 已启动

**步骤：**
1. 在 Windows Client 侧边栏输入命令

2. 观察 Galaxy Gateway Dashboard 的日志

3. 验证：
   - ✅ Dashboard 日志显示收到命令
   - ✅ Windows Client 显示执行结果

**预期结果：**
- 两个系统能正常通信
- 命令能正确路由和执行

---

### 测试 5: UI 树抓取

**目标：** 验证能正确抓取 Windows UI 树

**步骤：**
1. 打开任意应用（如记事本）

2. 在 Windows Client 输入：`屏幕`

3. 验证：
   - ✅ 显示当前窗口名称
   - ✅ 显示"UI 树已获取"

**预期结果：**
- 能正确识别当前窗口
- UI 树抓取功能正常

---

## 已知问题

### 1. Fn 键支持

**问题：** PyQt5 不直接支持 Fn 键，目前使用 F12 作为替代

**解决方案：** 在实际部署时，可以使用 `pynput` 或 `keyboard` 库来监听真正的 Fn 键

### 2. 静态文件路径

**问题：** Galaxy Gateway 的静态文件路径可能需要调整

**解决方案：** 确保 `galaxy_gateway/static/` 目录存在，并包含 `dashboard.html`

---

## 测试结果记录

| 测试项目 | 状态 | 备注 |
|---------|------|------|
| Windows Client UI | ⏳ 待测试 | |
| Windows 自主操纵 | ⏳ 待测试 | |
| Galaxy Gateway Dashboard | ⏳ 待测试 | |
| Windows Client 与 Gateway 集成 | ⏳ 待测试 | |
| UI 树抓取 | ⏳ 待测试 | |

**测试人员：** _____________  
**测试日期：** _____________  
**测试环境：** Windows ___

---

## 下一步

测试完成后：
1. 记录所有问题和 Bug
2. 修复发现的问题
3. 重新测试
4. 准备最终交付

---

**文档版本：** 1.0  
**最后更新：** 2026-01-22
