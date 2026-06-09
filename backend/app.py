from __future__ import annotations
import sys
import os

# จัดการ Path ให้ Python หาโมดูลใน backend เจอ
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

# Import ภายในโปรเจกต์
from api.router import api_router
from api.admin_router import router as admin_router
from config.logging_config import get_logger, setup_logging
from config.settings import get_settings
from scheduler.scheduler_service import SchedulerService

# --- Setup ---
setup_logging()
logger = get_logger("app")
settings = get_settings()

class ConnectionManager:
    """จัดการ WebSocket Connections ให้รองรับการ Broadcast"""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()
scheduler_service = SchedulerService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Trading Platform")
    scheduler_service.start()
    yield
    logger.warning("Stopping AI Trading Platform")
    scheduler_service.shutdown()

app = FastAPI(
    title=settings.APP_NAME, 
    version=settings.APP_VERSION, 
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router)
app.include_router(admin_router, prefix="/api", tags=["Admin"])

# --- WebSocket ---
@app.websocket("/ws/dashboard")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # นี่คือจุดที่คุณสามารถดึงข้อมูลจาก Service จริงมาส่ง
            data = {
                "agent_status": {"isActive": True, "currentTask": "Trading BTC/USDT"},
                "portfolio": {"balance": 25000.75, "pnl": 1500.20},
                "market_alerts": [
                    {"id": 1, "severity": "critical", "symbol": "BTC", "message": "High volatility!"}
                ]
            }
            await manager.broadcast(data)
            await asyncio.sleep(int(settings.POSITION_MONITOR_INTERVAL_SECONDS))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME, 
        "version": settings.APP_VERSION, 
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    # รันโดยอ้างอิงไฟล์ปัจจุบัน
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)