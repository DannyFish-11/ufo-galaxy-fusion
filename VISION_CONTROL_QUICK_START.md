# UFO³ Galaxy 视觉操控系统 - 快速开始

**版本**: 1.0.0  
**日期**: 2026-01-22

---

## 🚀 5 分钟快速开始

### 1. 克隆项目

```bash
git clone https://github.com/DannyFish-11/ufo-galaxy.git
cd ufo-galaxy
```

### 2. 安装依赖

```bash
# Python 依赖
sudo pip3 install fastapi uvicorn httpx pydantic pillow
sudo pip3 install pytesseract paddleocr opencv-python pyautogui
sudo pip3 install google-genai python-multipart

# 系统依赖
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
```

### 3. 配置环境变量

```bash
export GEMINI_API_KEY="your_gemini_api_key"
```

### 4. 启动服务（一键启动）

```bash
# 方式 1：使用启动脚本（推荐）
./start_vision_system.sh

# 方式 2：手动启动
cd nodes/Node_15_OCR && python3.11 main_enhanced.py &
cd nodes/Node_45_DesktopAuto && python3.11 main_enhanced.py &
cd nodes/Node_90_MultimodalVision && python3.11 main.py &
cd nodes/Node_91_MultimodalAgent && python3.11 main.py &
cd nodes/Node_92_AutoControl && python3.11 main.py &
cd galaxy_gateway && python3.11 gateway_service_v4.py
```

### 5. 测试

```bash
# 健康检查
curl http://localhost:8000/health

# 执行命令
curl -X POST http://localhost:8000/execute_vision_command \
  -H "Content-Type: application/json" \
  -d '{"command": "打开记事本", "platform": "windows", "use_vision": true}'
```

---

## 📖 使用示例

### 示例 1：打开应用

```python
import requests

response = requests.post("http://localhost:8000/execute_vision_command", json={
    "command": "打开微信",
    "platform": "windows",
    "use_vision": True
})

print(response.json())
```

### 示例 2：智能点击

```python
response = requests.post("http://localhost:8000/execute_vision_command", json={
    "command": "点击登录按钮",
    "platform": "windows",
    "use_vision": True
})

print(response.json())
```

### 示例 3：输入文本

```python
response = requests.post("http://localhost:8000/execute_command", json={
    "command": "输入 hello world",
    "platform": "windows"
})

print(response.json())
```

---

## 🔧 常见问题

### Q1: 找不到 Tesseract

**解决方案**:
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
```

### Q2: PaddleOCR 下载模型失败

**解决方案**:
```bash
# 设置代理或手动下载模型
export HTTP_PROXY=http://your_proxy:port
```

### Q3: pyautogui 无法截图

**解决方案**:
```bash
# 安装 X11 依赖
sudo apt-get install python3-tk python3-dev
```

### Q4: Gemini API 调用失败

**解决方案**:
```bash
# 检查 API Key
echo $GEMINI_API_KEY

# 测试 API
curl -H "Authorization: Bearer $GEMINI_API_KEY" \
  https://generativelanguage.googleapis.com/v1beta/models
```

---

## 📚 更多文档

- [完整交付文档](./VISION_CONTROL_SYSTEM_DELIVERY.md)
- [需求分析](./VISION_CONTROL_ANALYSIS.md)
- [系统集成分析](./SYSTEM_INTEGRATION_ANALYSIS.md)

---

## 🎊 完成！

现在您可以通过自然语言和视觉识别来操控您的电脑了！

**GitHub**: https://github.com/DannyFish-11/ufo-galaxy
