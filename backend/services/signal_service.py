from config.logging_config import get_logger
from models.signal import SignalModel
from repositories.signals_repository import SignalsRepository


class SignalService:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.repository = SignalsRepository()

    def save_signal(
        self,
        signal: SignalModel,
    ) -> dict:
        self.logger.info(
            "Saving signal %s",
            signal.symbol,
        )

        return self.repository.create_signal(signal)

    def get_signals(self) -> list[dict]:
        return self.repository.get_signals()