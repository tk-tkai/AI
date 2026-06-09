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


market_data_worker = MarketDataWorker()

news_worker = NewsWorker()

signal_worker = SignalWorker()

position_monitor_worker = (
    PositionMonitorWorker()
)

performance_worker = (
    PerformanceWorker()
)