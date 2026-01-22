# UFO³ Galaxy - 视觉识别和自动操控需求分析

## 📋 用户需求

**核心问题：**
> "就是目前的这个，它是否可以通过视觉识别来操控我电脑或者安卓上的各种 Agent，或者编程工具，比如说 opencode"

**关键需求：**
1. **视觉识别** - 理解屏幕上的内容（UI 元素、文本、图标）
2. **自动操控** - 自动执行操作（点击、输入、滚动）
3. **跨平台支持** - Windows、Android
4. **应用支持** - VSCode、OpenCode、各种 App

---

## 🎯 目标场景

### 场景 1：操控编程工具

**用户命令：** "用 VSCode 打开这个项目"

**系统处理流程：**
1. **视觉识别**：截取屏幕，识别 VSCode 图标
2. **定位元素**：计算图标位置
3. **执行操作**：点击图标
4. **验证结果**：确认 VSCode 已打开
5. **后续操作**：识别文件菜单 → 点击 → 打开项目

---

### 场景 2：操控安卓应用

**用户命令：** "在手机上打开微信，找到张三的聊天"

**系统处理流程：**
1. **视觉识别**：截取手机屏幕，识别微信图标
2. **定位元素**：计算图标位置
3. **执行操作**：点击图标
4. **验证结果**：确认微信已打开
5. **后续操作**：识别搜索框 → 输入"张三" → 识别聊天列表 → 点击

---

### 场景 3：复杂的多步骤操作

**用户命令：** "用 OpenCode 打开 main.py，找到第 10 行，把 'hello' 改成 'world'"

**系统处理流程：**
1. **视觉识别**：识别 OpenCode 图标
2. **执行操作**：打开 OpenCode
3. **视觉识别**：识别文件树
4. **执行操作**：找到并点击 main.py
5. **视觉识别**：识别代码编辑器
6. **执行操作**：定位第 10 行
7. **视觉识别**：识别 'hello' 文本
8. **执行操作**：选中并替换为 'world'
9. **验证结果**：确认修改成功

---

## 🔍 当前系统能力分析

### 已有能力 ✅

1. **自然语言理解（NLU v2.0）**
   - 意图识别
   - 设备识别
   - 任务分解

2. **多设备通信（AIP v2.0）**
   - 统一的消息协议
   - 跨设备通信

3. **多模态传输**
   - 图片传输
   - 屏幕截图传输

4. **基础命令执行**
   - 通过 WebSocket 发送命令
   - 接收执行结果

### 缺少的能力 ❌

1. **视觉理解**
   - ❌ 屏幕内容分析
   - ❌ UI 元素识别
   - ❌ 文本识别（OCR）
   - ❌ 图标识别
   - ❌ 布局理解

2. **多模态 Agent**
   - ❌ 视觉 + 语言理解
   - ❌ 多模态 LLM 集成
   - ❌ 上下文理解

3. **自动操控**
   - ❌ 鼠标/触摸操作
   - ❌ 键盘输入
   - ❌ 元素定位
   - ❌ 操作验证

---

## 🛠️ 技术方案

### 1. 视觉理解模块（Vision Understanding）

#### 1.1 屏幕截图

**Windows：**
- 使用 `pyautogui` 或 `mss` 库
- 支持全屏和区域截图

**Android：**
- 使用 `adb shell screencap`
- 或使用 Android Accessibility Service

**实现：**
```python
import pyautogui
from PIL import Image

def capture_screen():
    """截取屏幕"""
    screenshot = pyautogui.screenshot()
    return screenshot

def capture_region(x, y, width, height):
    """截取屏幕区域"""
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    return screenshot
```

#### 1.2 UI 元素识别

**方案 1：基于模板匹配**
- 使用 OpenCV 的模板匹配
- 适合识别图标、按钮

**方案 2：基于 OCR**
- 使用 PaddleOCR 或 EasyOCR
- 适合识别文本

**方案 3：基于多模态 LLM**
- 使用 GPT-4V、Gemini、Qwen-VL
- 适合复杂的 UI 理解

**实现：**
```python
import cv2
import numpy as np
from paddleocr import PaddleOCR

class UIElementDetector:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    
    def detect_by_template(self, screenshot, template):
        """基于模板匹配检测元素"""
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return max_loc if max_val > 0.8 else None
    
    def detect_by_ocr(self, screenshot):
        """基于 OCR 检测文本"""
        result = self.ocr.ocr(screenshot, cls=True)
        return result
```

#### 1.3 多模态 LLM 集成

**支持的模型：**
- **GPT-4V** (OpenAI)
- **Gemini 2.0 Flash** (Google)
- **Qwen-VL** (Alibaba)
- **Claude 3.5** (Anthropic)

**实现：**
```python
from openai import OpenAI
from google import genai

class MultimodalLLM:
    def __init__(self, provider="gemini"):
        self.provider = provider
        
        if provider == "openai":
            self.client = OpenAI()
        elif provider == "gemini":
            self.client = genai.Client()
    
    def analyze_screen(self, screenshot, query):
        """分析屏幕并回答问题"""
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": query},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot}"}}
                        ]
                    }
                ]
            )
            return response.choices[0].message.content
        
        elif self.provider == "gemini":
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[query, screenshot]
            )
            return response.text
```

### 2. 多模态 Agent

#### 2.1 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    Multimodal Agent                         │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Vision    │  │   Language  │  │   Action    │        │
│  │ Understanding│ │ Understanding│ │  Planning   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│         │                 │                 │               │
│         └─────────────────┼─────────────────┘               │
│                           │                                 │
│                  ┌────────▼────────┐                        │
│                  │  Reasoning      │                        │
│                  │  Engine         │                        │
│                  └────────┬────────┘                        │
│                           │                                 │
│                  ┌────────▼────────┐                        │
│                  │  Action         │                        │
│                  │  Executor       │                        │
│                  └─────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

#### 2.2 推理流程

```python
class MultimodalAgent:
    def __init__(self):
        self.vision = VisionUnderstanding()
        self.language = LanguageUnderstanding()
        self.action_planner = ActionPlanner()
        self.executor = ActionExecutor()
    
    async def process(self, user_input, device_id):
        """处理用户输入"""
        # 1. 截取屏幕
        screenshot = await self.capture_screen(device_id)
        
        # 2. 视觉理解
        visual_context = await self.vision.analyze(screenshot)
        
        # 3. 语言理解
        intent = await self.language.understand(user_input)
        
        # 4. 推理和规划
        actions = await self.action_planner.plan(
            intent=intent,
            visual_context=visual_context,
            screenshot=screenshot
        )
        
        # 5. 执行操作
        results = []
        for action in actions:
            result = await self.executor.execute(action, device_id)
            results.append(result)
            
            # 验证结果
            if not result.success:
                # 重新截图和分析
                screenshot = await self.capture_screen(device_id)
                visual_context = await self.vision.analyze(screenshot)
                # 重新规划
                actions = await self.action_planner.replan(
                    action=action,
                    visual_context=visual_context
                )
        
        return results
```

### 3. 自动操控模块

#### 3.1 Windows 操控

**使用的库：**
- `pyautogui` - 鼠标和键盘操作
- `pywinauto` - Windows UI 自动化
- `uiautomation` - Windows UI Automation

**实现：**
```python
import pyautogui
import pywinauto

class WindowsController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
    
    def click(self, x, y):
        """点击指定位置"""
        pyautogui.click(x, y)
    
    def double_click(self, x, y):
        """双击指定位置"""
        pyautogui.doubleClick(x, y)
    
    def type_text(self, text):
        """输入文本"""
        pyautogui.typewrite(text, interval=0.05)
    
    def press_key(self, key):
        """按键"""
        pyautogui.press(key)
    
    def hotkey(self, *keys):
        """组合键"""
        pyautogui.hotkey(*keys)
    
    def scroll(self, clicks):
        """滚动"""
        pyautogui.scroll(clicks)
    
    def find_window(self, title):
        """查找窗口"""
        app = pywinauto.Application().connect(title=title)
        return app
    
    def find_element(self, window, element_name):
        """查找元素"""
        element = window.child_window(title=element_name)
        return element
```

#### 3.2 Android 操控

**方案 1：使用 ADB**
```python
import subprocess

class AndroidController:
    def __init__(self, device_id=None):
        self.device_id = device_id
    
    def _adb(self, command):
        """执行 ADB 命令"""
        if self.device_id:
            cmd = f"adb -s {self.device_id} {command}"
        else:
            cmd = f"adb {command}"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    
    def tap(self, x, y):
        """点击"""
        self._adb(f"shell input tap {x} {y}")
    
    def swipe(self, x1, y1, x2, y2, duration=300):
        """滑动"""
        self._adb(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")
    
    def type_text(self, text):
        """输入文本"""
        self._adb(f"shell input text '{text}'")
    
    def press_key(self, keycode):
        """按键"""
        self._adb(f"shell input keyevent {keycode}")
    
    def capture_screen(self):
        """截屏"""
        self._adb("shell screencap -p /sdcard/screenshot.png")
        self._adb("pull /sdcard/screenshot.png")
        return "screenshot.png"
```

**方案 2：使用 Accessibility Service**
```kotlin
// Android Agent 中实现
class AutoControlService : AccessibilityService() {
    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        // 处理可访问性事件
    }
    
    fun click(x: Int, y: Int) {
        val path = Path()
        path.moveTo(x.toFloat(), y.toFloat())
        
        val gesture = GestureDescription.Builder()
            .addStroke(GestureDescription.StrokeDescription(path, 0, 100))
            .build()
        
        dispatchGesture(gesture, null, null)
    }
    
    fun typeText(text: String) {
        val focusedNode = rootInActiveWindow.findFocus(AccessibilityNodeInfo.FOCUS_INPUT)
        focusedNode?.performAction(
            AccessibilityNodeInfo.ACTION_SET_TEXT,
            Bundle().apply { putCharSequence(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, text) }
        )
    }
    
    fun findElement(text: String): AccessibilityNodeInfo? {
        return rootInActiveWindow.findAccessibilityNodeInfosByText(text).firstOrNull()
    }
}
```

### 4. 元素定位策略

#### 4.1 基于视觉的定位

**步骤：**
1. 截取屏幕
2. 使用多模态 LLM 分析屏幕
3. 让 LLM 返回元素的位置（相对坐标或绝对坐标）
4. 计算实际坐标

**Prompt 示例：**
```
请分析这个屏幕截图，找到"VSCode"图标的位置。

请以 JSON 格式返回：
{
  "found": true,
  "element": "VSCode 图标",
  "position": {
    "x": 100,
    "y": 200,
    "width": 64,
    "height": 64
  },
  "confidence": 0.95
}
```

#### 4.2 基于 OCR 的定位

**步骤：**
1. 截取屏幕
2. 使用 OCR 识别所有文本
3. 找到目标文本
4. 返回文本的位置

**实现：**
```python
def find_text_position(screenshot, target_text):
    """查找文本位置"""
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    result = ocr.ocr(screenshot, cls=True)
    
    for line in result:
        for word_info in line:
            text = word_info[1][0]
            if target_text in text:
                box = word_info[0]
                x = int((box[0][0] + box[2][0]) / 2)
                y = int((box[0][1] + box[2][1]) / 2)
                return (x, y)
    
    return None
```

#### 4.3 基于模板匹配的定位

**步骤：**
1. 准备图标/元素的模板图片
2. 截取屏幕
3. 使用 OpenCV 模板匹配
4. 返回匹配位置

**实现：**
```python
import cv2

def find_by_template(screenshot, template_path):
    """基于模板匹配查找元素"""
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(template_path)
    
    result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val > 0.8:
        h, w = template.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y)
    
    return None
```

---

## 📊 技术选型

### 视觉理解

| 技术 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **多模态 LLM** | 理解能力强，泛化性好 | 速度慢，成本高 | 复杂 UI 理解 |
| **OCR** | 速度快，准确率高 | 只能识别文本 | 文本识别 |
| **模板匹配** | 速度快，简单 | 需要预先准备模板 | 图标识别 |
| **UI Automation** | 准确，可靠 | 需要应用支持 | Windows 应用 |

**推荐方案：** 混合使用
- **第一优先级**: 多模态 LLM（通用性强）
- **第二优先级**: OCR（文本识别）
- **第三优先级**: 模板匹配（图标识别）
- **第四优先级**: UI Automation（特定应用）

### 多模态 LLM

| 模型 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| **Gemini 2.0 Flash** | 速度快，免费额度高 | 需要 API key | ⭐⭐⭐⭐⭐ |
| **GPT-4o** | 理解能力强 | 成本高 | ⭐⭐⭐⭐ |
| **Qwen-VL** | 可本地部署 | 需要 GPU | ⭐⭐⭐ |
| **Claude 3.5** | 理解能力强 | 成本高 | ⭐⭐⭐⭐ |

**推荐方案：** Gemini 2.0 Flash（已有 API key）

### 自动操控

| 平台 | 技术 | 优点 | 缺点 |
|------|------|------|------|
| **Windows** | pyautogui | 简单易用 | 基于坐标 |
| **Windows** | pywinauto | 可靠，基于 UI 树 | 需要应用支持 |
| **Android** | ADB | 简单，通用 | 需要 USB 连接 |
| **Android** | Accessibility Service | 可靠，无需 USB | 需要权限 |

**推荐方案：**
- **Windows**: pyautogui（主要）+ pywinauto（辅助）
- **Android**: Accessibility Service（主要）+ ADB（辅助）

---

## 🎯 实现路线图

### Phase 1: 视觉理解模块（1-2 天）

1. **屏幕截图**
   - Windows: pyautogui
   - Android: ADB screencap

2. **OCR 集成**
   - PaddleOCR
   - 文本识别和定位

3. **多模态 LLM 集成**
   - Gemini 2.0 Flash
   - 屏幕分析和元素定位

### Phase 2: 多模态 Agent（2-3 天）

1. **Agent 架构**
   - 视觉理解
   - 语言理解
   - 推理引擎
   - 操作规划

2. **Prompt 工程**
   - 屏幕分析 Prompt
   - 元素定位 Prompt
   - 操作规划 Prompt

### Phase 3: 自动操控模块（2-3 天）

1. **Windows 控制器**
   - pyautogui 封装
   - 鼠标、键盘操作
   - 窗口管理

2. **Android 控制器**
   - Accessibility Service
   - 触摸、输入操作
   - 元素查找

### Phase 4: 集成和测试（1-2 天）

1. **集成到 Galaxy Gateway**
   - 新增视觉操控 API
   - WebSocket 消息扩展

2. **集成到 Android Agent**
   - Accessibility Service 实现
   - WebSocket 通信

3. **测试**
   - 单元测试
   - 集成测试
   - 端到端测试

---

## 📈 预期效果

### 性能指标

| 指标 | 目标值 |
|------|--------|
| 元素识别准确率 | > 90% |
| 操作成功率 | > 85% |
| 响应时间 | < 3 秒 |
| 多步骤任务成功率 | > 80% |

### 支持的操作

- ✅ 点击（图标、按钮、链接）
- ✅ 输入（文本框、搜索框）
- ✅ 滚动（页面、列表）
- ✅ 拖拽（文件、元素）
- ✅ 组合键（Ctrl+C、Ctrl+V）
- ✅ 多步骤操作（打开应用 → 查找 → 点击）

### 支持的应用

- ✅ VSCode
- ✅ OpenCode
- ✅ 浏览器（Chrome、Edge）
- ✅ 微信
- ✅ QQ
- ✅ 任意 Android App
- ✅ 任意 Windows 应用

---

## 🔒 安全考虑

### 权限控制

1. **用户确认**
   - 敏感操作需要用户确认
   - 例如：删除文件、发送消息

2. **操作日志**
   - 记录所有操作
   - 可审计

3. **沙箱模式**
   - 测试模式下不执行实际操作
   - 只返回模拟结果

### 隐私保护

1. **屏幕截图**
   - 只在需要时截图
   - 截图不保存到云端

2. **敏感信息**
   - 不记录密码、支付信息
   - 自动模糊处理

---

## 💡 未来扩展

### 短期（1-2 月）

1. **增强视觉理解**
   - 支持更多 UI 元素类型
   - 提高识别准确率

2. **增强操控能力**
   - 支持更多操作类型
   - 支持更多应用

### 中期（3-6 月）

1. **学习能力**
   - 从用户操作中学习
   - 自动生成操作脚本

2. **智能推荐**
   - 根据上下文推荐操作
   - 自动完成常见任务

### 长期（6-12 月）

1. **多模态对话**
   - 支持语音 + 视觉
   - 实时反馈

2. **跨应用协同**
   - 自动在多个应用间切换
   - 完成复杂的工作流

---

## 📚 参考资料

### 开源项目

1. **UFO (Microsoft)** - https://github.com/microsoft/UFO
   - Windows UI 自动化
   - 多模态 Agent

2. **AppAgent** - https://github.com/mnotgod96/AppAgent
   - Android 自动化
   - 视觉识别

3. **OpenAdapt** - https://github.com/OpenAdaptAI/OpenAdapt
   - 跨平台自动化
   - 学习用户操作

### 论文

1. **GPT-4V(ision) System Card** - OpenAI
2. **Gemini: A Family of Highly Capable Multimodal Models** - Google
3. **AppAgent: Multimodal Agents as Smartphone Users** - Tencent

---

## 🎊 总结

### 核心能力

1. **视觉理解** - 理解屏幕上的内容
2. **多模态推理** - 结合视觉和语言理解
3. **自动操控** - 执行操作并验证结果
4. **跨平台支持** - Windows 和 Android

### 技术栈

- **视觉**: Gemini 2.0 Flash + PaddleOCR + OpenCV
- **控制**: pyautogui + Accessibility Service
- **推理**: 多模态 Agent + Prompt 工程

### 预期效果

- **识别准确率**: > 90%
- **操作成功率**: > 85%
- **响应时间**: < 3 秒

---

**版本**: 1.0  
**日期**: 2026-01-22  
**作者**: Manus AI
