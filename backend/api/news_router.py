from fastapi import APIRouter

from services.news_service import (
    NewsService,
)

router = APIRouter(
    prefix="/api/news",
    tags=["News"],
)

news_service = NewsService()


@router.get("")
async def get_news() -> list[dict]:
    return news_service.get_news()