from __future__ import annotations

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from config.logging_config import get_logger
from config.settings import get_settings
from workers.market_data_worker import (
    MarketDataWorker,
)
from workers.news_worker import (
    NewsWorker,
)
from workers.performance_worker import (
    PerformanceWorker,
)
from workers.position_monitor_worker import (
    PositionMonitorWorker,
)
from workers.signal_worker import (
    SignalWorker,
)


class SchedulerService:
    def __init__(self) -> None:
        self.logger = get_logger(
            self.__class__.__name__
        )

        self.settings = get_settings()

        self.scheduler = AsyncIOScheduler(
            timezone="UTC"
        )

        self.market_worker = (
            MarketDataWorker()
        )

        self.news_worker = (
            NewsWorker()
        )

        self.signal_worker = (
            SignalWorker()
        )

        self.position_worker = (
            PositionMonitorWorker()
        )

        self.performance_worker = (
            PerformanceWorker()
        )

    def start(self) -> None:
        self.logger.info(
            "Starting scheduler"
        )

        self.scheduler.add_job(
            func=self.market_worker.run,
            trigger=IntervalTrigger(
                minutes=self.settings.MARKET_FETCH_INTERVAL_MINUTES
            ),
            id="market_data_job",
            replace_existing=True,
        )

        self.scheduler.add_job(
            func=self.news_worker.run,
            trigger=IntervalTrigger(
                minutes=self.settings.NEWS_FETCH_INTERVAL_MINUTES
            ),
            id="news_job",
            replace_existing=True,
        )

        self.scheduler.add_job(
            func=self._run_signal_generation,
            trigger=IntervalTrigger(
                minutes=self.settings.SIGNAL_GENERATION_INTERVAL_MINUTES
            ),
            id="signal_job",
            replace_existing=True,
        )

        self.scheduler.add_job(
            func=self.position_worker.run,
            trigger=IntervalTrigger(
                seconds=self.settings.POSITION_MONITOR_INTERVAL_SECONDS
            ),
            id="position_monitor_job",
            replace_existing=True,
        )

        self.scheduler.add_job(
            func=self._run_performance_update,
            trigger=IntervalTrigger(
                minutes=15
            ),
            id="performance_job",
            replace_existing=True,
        )

        self.scheduler.start()

        self.logger.info(
            "Scheduler started successfully"
        )

    def shutdown(self) -> None:
        self.logger.warning(
            "Stopping scheduler"
        )

        self.scheduler.shutdown(
            wait=False
        )

    def _run_signal_generation(
        self,
    ) -> None:
        self.signal_worker.run(
            news_text=(
                "Analyze latest market conditions, "
                "macro events, central bank activity, "
                "crypto adoption and risk sentiment."
            )
        )

    def _run_performance_update(
        self,
    ) -> None:
        initial_capital = 60.0
        self.performance_worker.run(
            balance=initial_capital,
            equity=initial_capital,
        )
        