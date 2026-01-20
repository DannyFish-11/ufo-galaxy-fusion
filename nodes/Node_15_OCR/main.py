"""Node 15: OCR - 文字识别"""
import os, base64
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Node 15 - OCR", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# 尝试导入 OCR 库
pytesseract = None
try:
    import pytesseract as _pytesseract
    pytesseract = _pytesseract
except ImportError:
    pass

easyocr_reader = None
try:
    import easyocr
    easyocr_reader = easyocr.Reader(['ch_sim', 'en'])
except ImportError:
    pass

class OCRRequest(BaseModel):
    image_path: Optional[str] = None
    image_base64: Optional[str] = None
    lang: str = "chi_sim+eng"

@app.get("/health")
async def health():
    return {"status": "healthy" if (pytesseract or easyocr_reader) else "degraded", "node_id": "15", "name": "OCR", "pytesseract": pytesseract is not None, "easyocr": easyocr_reader is not None, "timestamp": datetime.now().isoformat()}

@app.post("/recognize")
async def recognize(request: OCRRequest):
    try:
        from PIL import Image
        from io import BytesIO
        
        if request.image_path:
            img = Image.open(request.image_path)
        elif request.image_base64:
            img_data = base64.b64decode(request.image_base64)
            img = Image.open(BytesIO(img_data))
        else:
            raise HTTPException(status_code=400, detail="image_path or image_base64 required")
        
        # 优先使用 EasyOCR (中文效果更好)
        if easyocr_reader:
            import numpy as np
            result = easyocr_reader.readtext(np.array(img))
            text = "\n".join([item[1] for item in result])
            return {"success": True, "text": text, "engine": "easyocr", "details": [{"text": item[1], "confidence": item[2], "bbox": item[0]} for item in result]}
        
        # 使用 Tesseract
        if pytesseract:
            text = pytesseract.image_to_string(img, lang=request.lang)
            return {"success": True, "text": text, "engine": "tesseract"}
        
        raise HTTPException(status_code=503, detail="No OCR engine available. Install pytesseract or easyocr.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/call")
async def mcp_call(request: dict):
    tool = request.get("tool", "")
    params = request.get("params", {})
    if tool == "recognize": return await recognize(OCRRequest(**params))
    raise HTTPException(status_code=400, detail=f"Unknown tool: {tool}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8015)
