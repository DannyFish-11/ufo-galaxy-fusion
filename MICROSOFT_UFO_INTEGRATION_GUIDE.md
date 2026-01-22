# 微软 UFO³ 增强集成指南

**目标**: 将我们开发的视觉增强功能（Qwen3-VL + Node_90）集成到您本地克隆的微软 UFO 项目中。

**适用场景**: 您已经在 Windows 本地克隆了微软 UFO 项目，现在希望为其添加多模态视觉理解能力。

---

## 📋 前提条件

1. ✅ 您已克隆微软 UFO 项目到本地（例如：`E:\UFO`）
2. ✅ 您已配置好 API 密钥（`OPENROUTER_API_KEY` 或 `GEMINI_API_KEY`）
3. ✅ Python 3.10+ 环境已就绪

---

## 🎯 集成方案：两种路径

### 路径 A：作为独立的 Galaxy 设备节点（推荐）⭐

**适合场景**: 您希望将视觉能力作为一个**独立的微服务**，通过 UFO³ 的 Galaxy 框架进行调用。

**优势**:
- 符合微软 UFO³ 的架构设计（Galaxy 多设备协调）
- 不修改 UFO 核心代码，易于维护
- 可以部署在不同设备上（如另一台服务器）

**集成步骤**:

#### 1. 在 UFO 项目中创建视觉节点目录

```powershell
cd E:\UFO
mkdir galaxy\devices\vision_node
```

#### 2. 复制 Node_90 代码到 UFO 项目

将我们开发的 `Node_90_MultimodalVision` 复制到 UFO 的设备目录：

```powershell
# 从我们的仓库复制
xcopy /E /I /Y "path\to\ufo-galaxy\nodes\Node_90_MultimodalVision" "E:\UFO\galaxy\devices\vision_node"
```

#### 3. 注册为 Galaxy 设备

在 `E:\UFO\config\galaxy\devices.yaml` 中添加：

```yaml
devices:
  - id: vision_node
    name: "Vision Understanding Node"
    type: "service"
    capabilities:
      - "visual_analysis"
      - "ocr"
      - "screen_capture"
    endpoint: "http://localhost:8090"
    protocol: "http"
```

#### 4. 启动视觉节点

```powershell
cd E:\UFO\galaxy\devices\vision_node
python main.py
```

#### 5. 在 Galaxy 中调用

现在您可以在 UFO³ 的 Galaxy 框架中通过自然语言调用视觉能力：

```python
# 在 UFO³ Galaxy 中
"请分析当前屏幕上的内容"
# Galaxy 会自动路由到 vision_node 设备
```

---

### 路径 B：集成到 UFO² Desktop AgentOS（深度集成）

**适合场景**: 您希望将视觉能力**深度集成**到 UFO² 的单设备自动化系统中。

**优势**:
- 视觉能力成为 UFO² 的原生功能
- 更低的调用延迟（无需跨设备通信）

**集成步骤**:

#### 1. 在 UFO² 中创建视觉自动化器

```powershell
cd E:\UFO\ufo\automator
mkdir vision_automator
```

#### 2. 创建视觉自动化器类

在 `E:\UFO\ufo\automator\vision_automator\__init__.py` 中：

```python
"""
视觉理解自动化器
集成 Qwen3-VL 和 Gemini 进行屏幕内容分析
"""

import os
from openai import OpenAI

class VisionAutomator:
    """视觉理解自动化器"""
    
    def __init__(self):
        # 初始化 OpenRouter 客户端（用于 Qwen3-VL）
        self.openrouter_client = None
        if os.getenv("OPENROUTER_API_KEY"):
            self.openrouter_client = OpenAI(
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1"
            )
        
        # 初始化 Gemini 客户端（备用）
        self.gemini_client = None
        if os.getenv("GEMINI_API_KEY"):
            from google import genai
            self.gemini_client = genai.Client(
                api_key=os.getenv("GEMINI_API_KEY")
            )
    
    def analyze_screen(self, image_path: str, query: str) -> str:
        """
        分析屏幕内容
        
        Args:
            image_path: 图片路径
            query: 分析查询
        
        Returns:
            分析结果文本
        """
        # 优先使用 Qwen3-VL
        if self.openrouter_client:
            return self._analyze_with_qwen(image_path, query)
        elif self.gemini_client:
            return self._analyze_with_gemini(image_path, query)
        else:
            raise ValueError("No VLM provider available")
    
    def _analyze_with_qwen(self, image_path: str, query: str) -> str:
        """使用 Qwen3-VL 分析"""
        # 上传图片到公共 URL
        import subprocess
        result = subprocess.run(
            ["manus-upload-file", image_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        image_url = result.stdout.strip()
        
        # 调用 Qwen3-VL
        response = self.openrouter_client.chat.completions.create(
            model="qwen/qwen3-vl-32b-instruct",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }],
            temperature=0.2,
            max_tokens=2048
        )
        
        return response.choices[0].message.content
    
    def _analyze_with_gemini(self, image_path: str, query: str) -> str:
        """使用 Gemini 分析"""
        from PIL import Image
        image = Image.open(image_path)
        
        response = self.gemini_client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=[query, image]
        )
        
        return response.text
```

#### 3. 在 AppAgent 中注册视觉能力

修改 `E:\UFO\ufo\agents\agent\app_agent.py`，添加视觉分析动作：

```python
from ufo.automator.vision_automator import VisionAutomator

class AppAgent:
    def __init__(self, ...):
        # ... 原有代码 ...
        self.vision_automator = VisionAutomator()
    
    def analyze_screen(self, query: str) -> str:
        """分析当前屏幕"""
        # 截取屏幕
        screenshot_path = self.capture_screenshot()
        
        # 调用视觉自动化器
        result = self.vision_automator.analyze_screen(
            screenshot_path,
            query
        )
        
        return result
```

#### 4. 在 Prompt 中添加视觉分析指令

修改 `E:\UFO\ufo\prompts\app_agent\api.yaml`，添加：

```yaml
- name: analyze_screen
  description: "分析当前屏幕内容，理解 UI 元素和文本信息"
  parameters:
    - name: query
      type: string
      description: "分析查询，例如：'这个屏幕上显示的是什么？'"
  returns: "屏幕内容的文本描述"
```

---

## 🔄 两种路径的对比

| 维度 | 路径 A（Galaxy 设备节点） | 路径 B（UFO² 深度集成） |
| :--- | :--- | :--- |
| **集成难度** | ⭐⭐ 简单（无需修改 UFO 核心） | ⭐⭐⭐⭐ 复杂（需要修改多个文件） |
| **架构符合度** | ✅ 完全符合 UFO³ Galaxy 设计 | ⚠️ 需要适配 UFO² 架构 |
| **部署灵活性** | ✅ 可独立部署在不同设备 | ❌ 必须与 UFO² 在同一设备 |
| **调用延迟** | ⚠️ 稍高（HTTP 调用） | ✅ 最低（进程内调用） |
| **维护成本** | ✅ 低（独立模块） | ⚠️ 高（与 UFO 耦合） |

---

## 💡 我的推荐

**如果您的目标是实现跨设备控制**（如您之前提到的"Windows 主节点 + 手机 A + 手机 B"），我强烈推荐**路径 A（Galaxy 设备节点）**。

原因：
1. ✅ 符合微软 UFO³ 的 Galaxy 架构设计
2. ✅ 视觉节点可以部署在任意设备上（甚至可以是云端服务器）
3. ✅ 其他设备（手机 A、手机 B）也可以通过 Galaxy 调用视觉节点
4. ✅ 易于扩展（未来可以添加更多节点，如语音识别、图像生成等）

---

## 🚀 快速验证脚本

无论您选择哪种路径，都可以先用这个脚本验证视觉能力是否可用：

```python
# test_vision.py
import os
from openai import OpenAI

# 测试 OpenRouter + Qwen3-VL
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

response = client.chat.completions.create(
    model="qwen/qwen3-vl-32b-instruct",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "这是什么？"},
            {"type": "image_url", "image_url": {"url": "https://example.com/test.jpg"}}
        ]
    }]
)

print(response.choices[0].message.content)
```

---

## 📞 后续支持

如果您在集成过程中遇到任何问题，请告诉我：
1. 您选择了哪种集成路径？
2. 在哪一步遇到了问题？
3. 错误信息是什么？

我会为您提供针对性的解决方案。

---

**最后提醒**：
- 所有代码已推送到 `DannyFish-11/ufo-galaxy` 仓库
- 您可以随时从 GitHub 拉取最新代码
- 建议先在测试环境中验证，再部署到生产环境
