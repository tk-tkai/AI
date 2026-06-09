from fastapi import APIRouter

from services.signal_service import (
    SignalService,
)

router = APIRouter(
    prefix="/api/signals",
    tags=["Signals"],
)

signal_service = SignalService()


@router.get("")
async def get_signals() -> list[dict]:
    return signal_service.get_signals()