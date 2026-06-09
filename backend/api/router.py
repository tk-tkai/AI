from fastapi import APIRouter

from api.health_router import (
    router as health_router,
)
from api.market_router import (
    router as market_router,
)
from api.news_router import (
    router as news_router,
)
from api.paper_trading_router import (
    router as paper_router,
)
from api.performance_router import (
    router as performance_router,
)
from api.signals_router import (
    router as signals_router,
)

api_router = APIRouter()

api_router.include_router(
    health_router
)

api_router.include_router(
    signals_router
)

api_router.include_router(
    performance_router
)

api_router.include_router(
    paper_router
)

api_router.include_router(
    market_router
)

api_router.include_router(
    news_router
)