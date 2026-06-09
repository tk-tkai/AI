from __future__ import annotations

from config.logging_config import get_logger
from models.paper_position import PaperPositionModel
from models.paper_trade import PaperTradeModel
from models.performance_stats import PerformanceStatsModel
from repositories.paper_positions_repository import (
    PaperPositionsRepository,
)
from repositories.paper_trades_repository import (
    PaperTradesRepository,
)


class PaperTradeService:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)

        self.positions_repository = (
            PaperPositionsRepository()
        )

        self.trades_repository = (
            PaperTradesRepository()
        )

    def open_position(
        self,
        position: PaperPositionModel,
    ) -> dict:
        self.logger.info(
            "Opening position %s",
            position.symbol,
        )

        return self.positions_repository.create_position(
            position
        )

    def close_position(
        self,
        trade: PaperTradeModel,
        position_id: str,
    ) -> dict:
        self.logger.info(
            "Closing position %s",
            position_id,
        )

        self.positions_repository.update_position(
            position_id=position_id,
            payload={
                "status": "CLOSED",
                "closed_at": trade.closed_at.isoformat(),
            },
        )

        return self.trades_repository.create_trade(
            trade
        )

    def calculate_position_pnl(
        self,
        side: str,
        entry_price: float,
        current_price: float,
        quantity: float,
    ) -> float:
        if side == "BUY":
            return (
                current_price - entry_price
            ) * quantity

        return (
            entry_price - current_price
        ) * quantity

    def calculate_performance(
        self,
        trades: list[PaperTradeModel],
        balance: float,
        equity: float,
    ) -> PerformanceStatsModel:
        total_trades = len(trades)

        if total_trades == 0:
            return PerformanceStatsModel(
                equity=equity,
                balance=balance,
                win_rate=0,
                profit_factor=0,
                total_trades=0,
                average_rr=0,
                max_drawdown=0,
            )

        wins = [
            trade
            for trade in trades
            if trade.pnl > 0
        ]

        losses = [
            trade
            for trade in trades
            if trade.pnl < 0
        ]

        gross_profit = sum(
            trade.pnl
            for trade in wins
        )

        gross_loss = abs(
            sum(
                trade.pnl
                for trade in losses
            )
        )

        profit_factor = (
            gross_profit / gross_loss
            if gross_loss > 0
            else gross_profit
        )

        average_rr = (
            sum(
                trade.rr
                for trade in trades
            )
            / total_trades
        )

        win_rate = (
            len(wins)
            / total_trades
        ) * 100

        running_equity = balance
        peak = balance
        max_drawdown = 0.0

        for trade in trades:
            running_equity += trade.pnl

            if running_equity > peak:
                peak = running_equity

            drawdown = (
                (peak - running_equity)
                / peak
            ) * 100

            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return PerformanceStatsModel(
            equity=equity,
            balance=balance,
            win_rate=round(win_rate, 2),
            profit_factor=round(
                profit_factor,
                2,
            ),
            total_trades=total_trades,
            average_rr=round(
                average_rr,
                2,
            ),
            max_drawdown=round(
                max_drawdown,
                2,
            ),
        )