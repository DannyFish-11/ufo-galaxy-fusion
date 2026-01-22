"""
UFO³ Galaxy - 视觉理解模块

功能：
1. 屏幕截图
2. UI 元素识别
3. OCR 文本识别
4. 多模态 LLM 分析

作者：Manus AI
日期：2026-01-22
版本：1.0
"""

import asyncio
import base64
import io
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any

import cv2
import numpy as np
from PIL import Image

# 多模态 LLM
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# OCR
try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False

# ============================================================================
# 数据类
# ============================================================================

class ElementType(Enum):
    """UI 元素类型"""
    BUTTON = "button"
    TEXT = "text"
    INPUT = "input"
    IMAGE = "image"
    ICON = "icon"
    MENU = "menu"
    WINDOW = "window"
    UNKNOWN = "unknown"

@dataclass
class BoundingBox:
    """边界框"""
    x: int
    y: int
    width: int
    height: int
    
    @property
    def center(self) -> Tuple[int, int]:
        """中心点"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    @property
    def top_left(self) -> Tuple[int, int]:
        """左上角"""
        return (self.x, self.y)
    
    @property
    def bottom_right(self) -> Tuple[int, int]:
        """右下角"""
        return (self.x + self.width, self.y + self.height)

@dataclass
class UIElement:
    """UI 元素"""
    element_type: ElementType
    text: str
    bounding_box: BoundingBox
    confidence: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class ScreenAnalysis:
    """屏幕分析结果"""
    screenshot: Image.Image
    elements: List[UIElement]
    description: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

# ============================================================================
# 屏幕截图
# ============================================================================

class ScreenCapture:
    """屏幕截图"""
    
    @staticmethod
    def capture_windows() -> Image.Image:
        """截取 Windows 屏幕"""
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            return screenshot
        except ImportError:
            raise RuntimeError("pyautogui not installed. Run: pip install pyautogui")
    
    @staticmethod
    def capture_android(device_id: str = None) -> Image.Image:
        """截取 Android 屏幕"""
        import subprocess
        import tempfile
        
        # 使用 ADB 截图
        if device_id:
            cmd_prefix = f"adb -s {device_id}"
        else:
            cmd_prefix = "adb"
        
        # 截图到设备
        subprocess.run(f"{cmd_prefix} shell screencap -p /sdcard/screenshot.png", shell=True)
        
        # 拉取到本地
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            temp_file = f.name
        
        subprocess.run(f"{cmd_prefix} pull /sdcard/screenshot.png {temp_file}", shell=True)
        
        # 读取图片
        screenshot = Image.open(temp_file)
        
        # 清理
        os.remove(temp_file)
        
        return screenshot
    
    @staticmethod
    def capture_region(x: int, y: int, width: int, height: int, platform: str = "windows") -> Image.Image:
        """截取屏幕区域"""
        if platform == "windows":
            try:
                import pyautogui
                screenshot = pyautogui.screenshot(region=(x, y, width, height))
                return screenshot
            except ImportError:
                raise RuntimeError("pyautogui not installed")
        else:
            raise NotImplementedError(f"Region capture not implemented for {platform}")

# ============================================================================
# OCR 文本识别
# ============================================================================

class OCREngine:
    """OCR 引擎"""
    
    def __init__(self, lang: str = "ch"):
        """初始化
        
        Args:
            lang: 语言（ch=中文，en=英文）
        """
        if not PADDLEOCR_AVAILABLE:
            raise RuntimeError("PaddleOCR not installed. Run: pip install paddleocr")
        
        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang, show_log=False)
    
    def detect_text(self, image: Image.Image) -> List[UIElement]:
        """检测文本
        
        Args:
            image: 图片
        
        Returns:
            UI 元素列表
        """
        # 转换为 numpy 数组
        img_array = np.array(image)
        
        # OCR 识别
        result = self.ocr.ocr(img_array, cls=True)
        
        # 解析结果
        elements = []
        
        if result and result[0]:
            for line in result[0]:
                # 边界框
                box = line[0]
                x_min = int(min([p[0] for p in box]))
                y_min = int(min([p[1] for p in box]))
                x_max = int(max([p[0] for p in box]))
                y_max = int(max([p[1] for p in box]))
                
                bounding_box = BoundingBox(
                    x=x_min,
                    y=y_min,
                    width=x_max - x_min,
                    height=y_max - y_min
                )
                
                # 文本和置信度
                text = line[1][0]
                confidence = line[1][1]
                
                # 创建元素
                element = UIElement(
                    element_type=ElementType.TEXT,
                    text=text,
                    bounding_box=bounding_box,
                    confidence=confidence
                )
                
                elements.append(element)
        
        return elements
    
    def find_text(self, image: Image.Image, target_text: str) -> Optional[UIElement]:
        """查找文本
        
        Args:
            image: 图片
            target_text: 目标文本
        
        Returns:
            UI 元素（如果找到）
        """
        elements = self.detect_text(image)
        
        for element in elements:
            if target_text in element.text:
                return element
        
        return None

# ============================================================================
# 模板匹配
# ============================================================================

class TemplateMatching:
    """模板匹配"""
    
    @staticmethod
    def find_template(screenshot: Image.Image, template_path: str, threshold: float = 0.8) -> Optional[BoundingBox]:
        """查找模板
        
        Args:
            screenshot: 屏幕截图
            template_path: 模板图片路径
            threshold: 匹配阈值
        
        Returns:
            边界框（如果找到）
        """
        # 转换为 OpenCV 格式
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        template = cv2.imread(template_path)
        
        if template is None:
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        # 模板匹配
        result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # 检查阈值
        if max_val >= threshold:
            h, w = template.shape[:2]
            return BoundingBox(
                x=max_loc[0],
                y=max_loc[1],
                width=w,
                height=h
            )
        
        return None

# ============================================================================
# 多模态 LLM
# ============================================================================

class MultimodalLLM:
    """多模态 LLM"""
    
    def __init__(self, provider: str = "gemini", model: str = None):
        """初始化
        
        Args:
            provider: 提供商（gemini, openai）
            model: 模型名称
        """
        self.provider = provider
        
        if provider == "gemini":
            if not GEMINI_AVAILABLE:
                raise RuntimeError("Google GenAI not installed. Run: pip install google-genai")
            
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise RuntimeError("GEMINI_API_KEY not set")
            
            self.client = genai.Client(api_key=api_key)
            self.model = model or "gemini-2.0-flash-exp"
        
        elif provider == "openai":
            if not OPENAI_AVAILABLE:
                raise RuntimeError("OpenAI not installed. Run: pip install openai")
            
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError("OPENAI_API_KEY not set")
            
            self.client = OpenAI(api_key=api_key)
            self.model = model or "gpt-4o"
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _image_to_base64(self, image: Image.Image) -> str:
        """图片转 Base64"""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    async def analyze_screen(self, screenshot: Image.Image, query: str) -> str:
        """分析屏幕
        
        Args:
            screenshot: 屏幕截图
            query: 查询
        
        Returns:
            分析结果
        """
        if self.provider == "gemini":
            # 使用 Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=[query, screenshot]
            )
            return response.text
        
        elif self.provider == "openai":
            # 使用 OpenAI
            image_base64 = self._image_to_base64(screenshot)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": query},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ]
            )
            
            return response.choices[0].message.content
    
    async def find_element(self, screenshot: Image.Image, element_description: str) -> Optional[Dict[str, Any]]:
        """查找元素
        
        Args:
            screenshot: 屏幕截图
            element_description: 元素描述
        
        Returns:
            元素信息（JSON 格式）
        """
        query = f"""请分析这个屏幕截图，找到"{element_description}"的位置。

请以 JSON 格式返回（不要使用 markdown 代码块）：
{{
  "found": true/false,
  "element": "元素名称",
  "position": {{
    "x": 相对于屏幕左上角的 x 坐标,
    "y": 相对于屏幕左上角的 y 坐标,
    "width": 元素宽度,
    "height": 元素高度
  }},
  "confidence": 0.0-1.0,
  "description": "元素的详细描述"
}}

如果找不到，请返回：
{{
  "found": false,
  "reason": "未找到的原因"
}}
"""
        
        response = await self.analyze_screen(screenshot, query)
        
        # 解析 JSON
        import json
        
        # 清理响应（移除可能的 markdown 代码块）
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        try:
            result = json.loads(response)
            return result
        except json.JSONDecodeError as e:
            print(f"JSON 解析错误: {e}")
            print(f"响应: {response}")
            return None

# ============================================================================
# 视觉理解管理器
# ============================================================================

class VisionUnderstanding:
    """视觉理解管理器"""
    
    def __init__(self, llm_provider: str = "gemini", ocr_lang: str = "ch"):
        """初始化
        
        Args:
            llm_provider: LLM 提供商
            ocr_lang: OCR 语言
        """
        self.screen_capture = ScreenCapture()
        
        # OCR（可选）
        try:
            self.ocr = OCREngine(lang=ocr_lang)
        except RuntimeError:
            print("警告: PaddleOCR 未安装，OCR 功能不可用")
            self.ocr = None
        
        # 多模态 LLM
        try:
            self.llm = MultimodalLLM(provider=llm_provider)
        except RuntimeError as e:
            print(f"警告: {e}")
            self.llm = None
    
    async def analyze(self, screenshot: Image.Image, query: str = None) -> ScreenAnalysis:
        """分析屏幕
        
        Args:
            screenshot: 屏幕截图
            query: 查询（可选）
        
        Returns:
            屏幕分析结果
        """
        elements = []
        description = ""
        
        # OCR 识别
        if self.ocr:
            text_elements = self.ocr.detect_text(screenshot)
            elements.extend(text_elements)
        
        # LLM 分析
        if self.llm and query:
            description = await self.llm.analyze_screen(screenshot, query)
        elif self.llm:
            # 默认查询
            default_query = "请描述这个屏幕上的主要内容和 UI 元素。"
            description = await self.llm.analyze_screen(screenshot, default_query)
        
        return ScreenAnalysis(
            screenshot=screenshot,
            elements=elements,
            description=description
        )
    
    async def find_element_by_description(
        self,
        screenshot: Image.Image,
        element_description: str
    ) -> Optional[UIElement]:
        """通过描述查找元素
        
        Args:
            screenshot: 屏幕截图
            element_description: 元素描述
        
        Returns:
            UI 元素（如果找到）
        """
        if not self.llm:
            raise RuntimeError("LLM not available")
        
        result = await self.llm.find_element(screenshot, element_description)
        
        if result and result.get("found"):
            position = result["position"]
            
            return UIElement(
                element_type=ElementType.UNKNOWN,
                text=result.get("element", element_description),
                bounding_box=BoundingBox(
                    x=position["x"],
                    y=position["y"],
                    width=position["width"],
                    height=position["height"]
                ),
                confidence=result.get("confidence", 0.0),
                metadata={
                    "description": result.get("description", "")
                }
            )
        
        return None
    
    async def find_element_by_text(
        self,
        screenshot: Image.Image,
        text: str
    ) -> Optional[UIElement]:
        """通过文本查找元素
        
        Args:
            screenshot: 屏幕截图
            text: 文本
        
        Returns:
            UI 元素（如果找到）
        """
        if not self.ocr:
            raise RuntimeError("OCR not available")
        
        return self.ocr.find_text(screenshot, text)
    
    def find_element_by_template(
        self,
        screenshot: Image.Image,
        template_path: str,
        threshold: float = 0.8
    ) -> Optional[UIElement]:
        """通过模板查找元素
        
        Args:
            screenshot: 屏幕截图
            template_path: 模板路径
            threshold: 匹配阈值
        
        Returns:
            UI 元素（如果找到）
        """
        bounding_box = TemplateMatching.find_template(screenshot, template_path, threshold)
        
        if bounding_box:
            return UIElement(
                element_type=ElementType.ICON,
                text=Path(template_path).stem,
                bounding_box=bounding_box,
                confidence=1.0
            )
        
        return None

# ============================================================================
# 示例用法
# ============================================================================

async def example_usage():
    """示例用法"""
    print("="*80)
    print("视觉理解模块 - 示例用法")
    print("="*80)
    
    # 创建视觉理解管理器
    vision = VisionUnderstanding(llm_provider="gemini")
    
    # 截取屏幕
    print("\n1. 截取屏幕...")
    screenshot = ScreenCapture.capture_windows()
    print(f"   屏幕大小: {screenshot.size}")
    
    # 分析屏幕
    print("\n2. 分析屏幕...")
    analysis = await vision.analyze(screenshot, "请描述这个屏幕上的主要内容")
    print(f"   描述: {analysis.description[:100]}...")
    print(f"   识别到 {len(analysis.elements)} 个文本元素")
    
    # 查找元素
    print("\n3. 查找元素...")
    element = await vision.find_element_by_description(screenshot, "开始菜单按钮")
    if element:
        print(f"   找到元素: {element.text}")
        print(f"   位置: {element.bounding_box.center}")
        print(f"   置信度: {element.confidence}")
    else:
        print("   未找到元素")
    
    print("\n完成！")

if __name__ == "__main__":
    asyncio.run(example_usage())
