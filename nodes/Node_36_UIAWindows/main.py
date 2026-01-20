"""Node 36: UIAWindows - Windows UI Automation"""
import os, subprocess
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Node 36 - UIAWindows", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class UIATools:
    def __init__(self):
        self.initialized = True
    def get_tools(self):
        return [
            {"name": "click", "description": "点击元素", "parameters": {"x": "X坐标", "y": "Y坐标"}},
            {"name": "type_text", "description": "输入文本", "parameters": {"text": "文本内容"}},
            {"name": "press_key", "description": "按键", "parameters": {"key": "按键名称"}},
            {"name": "screenshot", "description": "截图", "parameters": {}}
        ]
    async def call_tool(self, tool: str, params: dict):
        if tool == "click":
            # 使用 pyautogui 点击
            try:
                import pyautogui
                pyautogui.click(params.get("x", 0), params.get("y", 0))
                return {"success": True, "message": f"已点击 ({params.get('x')}, {params.get('y')})"}
            except Exception as e:
                return {"error": str(e)}
        elif tool == "type_text":
            try:
                import pyautogui
                pyautogui.write(params.get("text", ""))
                return {"success": True, "message": f"已输入文本"}
            except Exception as e:
                return {"error": str(e)}
        elif tool == "press_key":
            try:
                import pyautogui
                pyautogui.press(params.get("key", "enter"))
                return {"success": True, "message": f"已按下 {params.get('key')}"}
            except Exception as e:
                return {"error": str(e)}
        elif tool == "screenshot":
            try:
                import pyautogui
                screenshot = pyautogui.screenshot()
                path = f"/tmp/screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot.save(path)
                return {"success": True, "path": path}
            except Exception as e:
                return {"error": str(e)}
        return {"error": "Unknown tool"}

tools = UIATools()

@app.get("/health")
async def health():
    return {"status": "healthy", "node_id": "36", "name": "UIAWindows", "timestamp": datetime.now().isoformat()}

@app.get("/tools")
async def list_tools():
    return {"tools": tools.get_tools()}

@app.post("/mcp/call")
async def mcp_call(request: dict):
    try:
        return {"success": True, "result": await tools.call_tool(request.get("tool"), request.get("params", {}))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8036)
