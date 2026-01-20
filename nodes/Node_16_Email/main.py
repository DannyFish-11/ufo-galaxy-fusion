"""
Node 16: Email
====================
邮件发送
"""

import os
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Node 16 - Email", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class EmailTools:
    def __init__(self):
        
        import smtplib
        from email.mime.text import MIMEText
        
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_pass = os.getenv("SMTP_PASS", "")
        
    async def _tool_send(self, params):
        try:
            msg = MIMEText(params.get("body", ""))
            msg["Subject"] = params.get("subject", "")
            msg["From"] = self.smtp_user
            msg["To"] = params.get("to", "")
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_pass)
                server.send_message(msg)
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

        self.initialized = True
        
    def get_tools(self):
        return [
            {"name": "send", "description": "发送邮件", "parameters": {'to': '收件人', 'subject': '主题', 'body': '正文'}}
        ]
        
    async def call_tool(self, tool: str, params: dict):
        if not self.initialized:
            raise RuntimeError("Email not initialized")
        handler = getattr(self, f"_tool_{tool}", None)
        if not handler:
            raise ValueError(f"Unknown tool: {tool}")
        return await handler(params)

tools = EmailTools()

@app.get("/health")
async def health():
    return {"status": "healthy" if tools.initialized else "degraded", "node_id": "16", "name": "Email", "timestamp": datetime.now().isoformat()}

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
    uvicorn.run(app, host="0.0.0.0", port=8016)
