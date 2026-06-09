from fastapi import APIRouter

from workers.news_worker import NewsWorker

router = APIRouter()

@router.post("/admin/news/run")
async def run_news_worker() -> dict:
    worker = NewsWorker()
    worker.run()

    return {
        "status": "success",
        "message": "News worker executed"
    }