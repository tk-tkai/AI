from models.signal import SignalModel
from repositories.base_repository import BaseRepository


class SignalsRepository(BaseRepository):
    TABLE_NAME: str = "signals"

    def create_signal(
        self,
        signal: SignalModel,
    ) -> dict:
        return self.insert(
            self.TABLE_NAME,
            signal.model_dump(),
        )

    def get_signals(self) -> list[dict]:
        return self.get_all(
            self.TABLE_NAME,
        )

    def get_signal_by_id(
        self,
        signal_id: str,
    ) -> dict | None:
        return self.get_by_id(
            self.TABLE_NAME,
            signal_id,
        )