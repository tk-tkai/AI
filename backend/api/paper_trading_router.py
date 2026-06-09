from fastapi import APIRouter

from models.paper_position import (
    PaperPositionModel,
)
from orchestrator.paper_trading_orchestrator import (
    PaperTradingOrchestrator,
)

router = APIRouter(
    prefix="/api/paper",
    tags=["Paper Trading"],
)

orchestrator = (
    PaperTradingOrchestrator()
)


@router.post(
    "/buy"
)
async def open_buy(
    symbol: str,
    entry_price: float,
    sl: float,
    tp: float,
    quantity: float,
) -> dict:
    return orchestrator.open_trade(
        symbol=symbol,
        side="BUY",
        entry_price=entry_price,
        sl=sl,
        tp=tp,
        quantity=quantity,
    )


@router.post(
    "/sell"
)
async def open_sell(
    symbol: str,
    entry_price: float,
    sl: float,
    tp: float,
    quantity: float,
) -> dict:
    return orchestrator.open_trade(
        symbol=symbol,
        side="SELL",
        entry_price=entry_price,
        sl=sl,
        tp=tp,
        quantity=quantity,
    )


@router.get(
    "/positions"
)
async def positions() -> list[dict]:
    from repositories.paper_positions_repository import (
        PaperPositionsRepository,
    )

    repository = (
        PaperPositionsRepository()
    )

    return repository.get_positions()