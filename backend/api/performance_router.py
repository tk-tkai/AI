from fastapi import APIRouter

from services.performance_service import (
    PerformanceService,
)

router = APIRouter(
    prefix="/api",
    tags=["Performance"],
)

performance_service = (
    PerformanceService()
)


@router.get(
    "/performance"
)
async def get_performance() -> dict:
    stats = (
        performance_service.get_stats()
    )

    if not stats:
        return {
            "equity": 10000,
            "balance": 10000,
            "win_rate": 0,
            "profit_factor": 0,
            "max_drawdown": 0,
        }

    latest = stats[-1]

    return {
        "equity": latest["equity"],
        "balance": latest["balance"],
        "win_rate": latest["win_rate"],
        "profit_factor": latest["profit_factor"],
        "max_drawdown": latest["max_drawdown"],
    }