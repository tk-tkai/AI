from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.settings import get_settings


def build_scheduler() -> AsyncIOScheduler:
    settings = get_settings()

    scheduler = AsyncIOScheduler(
        timezone="UTC"
    )

    scheduler.configure(
        job_defaults={
            "coalesce": True,
            "max_instances": 1,
            "misfire_grace_time": 60,
        }
    )

    scheduler.add_jobstore(
        "memory"
    )

    _ = settings

    return scheduler