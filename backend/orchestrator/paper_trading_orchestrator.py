from __future__ import annotations

from datetime import UTC, datetime

from config.logging_config import get_logger
from models.paper_position import PaperPositionModel
from models.paper_trade import PaperTradeModel
from services.market_data_service import MarketDataService
from services.paper_trade_service import PaperTradeService


class PaperTradingOrchestrator:
    def __init__(self) -> None:
        self.logger = get_logger(
            self.__class__.__name__
        )

        self.paper_trade_service = (
            PaperTradeService()
        )

        self.market_service = (
            MarketDataService()
        )

    def open_trade(
        self,
        symbol: str,
        side: str,
        entry_price: float,
        sl: float,
        tp: float,
        quantity: float,
    ) -> dict:
        position = PaperPositionModel(
            symbol=symbol,
            side=side,
            entry_price=entry_price,
            current_price=entry_price,
            sl=sl,
            tp=tp,
            quantity=quantity,
        )

        return self.paper_trade_service.open_position(
            position
        )

    def monitor_position(
        self,
        position: PaperPositionModel,
    ) -> bool:
        latest_price = (
            self.market_service.get_latest_price(
                position.symbol
            )
        )

        self.logger.info(
            "MONITOR symbol=%s side=%s entry=%s sl=%s tp=%s latest=%s",
            position.symbol,
            position.side,
            position.entry_price,
            position.sl,
            position.tp,
            latest_price,
        )

        if position.side == "BUY":
            if latest_price >= position.tp:
                self._close_position(
                    position,
                    latest_price,
                    "WIN",
                )
                return True

            if latest_price <= position.sl:
                self._close_position(
                    position,
                    latest_price,
                    "LOSS",
                )
                return True

        elif position.side == "SELL":
            if latest_price <= position.tp:
                self._close_position(
                    position,
                    latest_price,
                    "WIN",
                )
                return True

            if latest_price >= position.sl:
                self._close_position(
                    position,
                    latest_price,
                    "LOSS",
                )
                return True

        return False

    def _close_position(
        self,
        position: PaperPositionModel,
        exit_price: float,
        result: str,
    ) -> None:
        pnl = (
            self.paper_trade_service
            .calculate_position_pnl(
                side=position.side,
                entry_price=position.entry_price,
                current_price=exit_price,
                quantity=position.quantity,
            )
        )

        self.logger.info(
            "CLOSE TRADE symbol=%s side=%s entry=%s exit=%s pnl=%s result=%s",
            position.symbol,
            position.side,
            position.entry_price,
            exit_price,
            pnl,
            result,
        )

        risk = abs(
            position.entry_price
            - position.sl
        )

        reward = abs(
            position.tp
            - position.entry_price
        )

        rr = (
            reward / risk
            if risk > 0
            else 0
        )

        trade = PaperTradeModel(
            position_id=position.id,
            symbol=position.symbol,
            side=position.side,
            entry_price=position.entry_price,
            exit_price=exit_price,
            quantity=position.quantity,
            pnl=pnl,
            rr=rr,
            result=result,
            opened_at=position.opened_at,
            closed_at=datetime.now(UTC),
        )

        self.paper_trade_service.close_position(
            trade=trade,
            position_id=position.id,
        )