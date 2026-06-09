from fastapi import APIRouter

from services.market_data_service import (
    MarketDataService,
)

router = APIRouter(
    prefix="/api/market",
    tags=["Market"],
)

market_service = (
    MarketDataService()
)


@router.get(
    "/price/{symbol}"
)
async def get_price(
    symbol: str,
) -> dict:
    return {
        "symbol": symbol,
        "price": market_service.get_latest_price(
            symbol
        ),
    }