from models.paper_trade import PaperTradeModel
from repositories.base_repository import BaseRepository


class PaperTradesRepository(BaseRepository):
    TABLE_NAME: str = "paper_trades"

    def create_trade(
        self,
        trade: PaperTradeModel,
    ) -> dict:
        return self.insert(
            self.TABLE_NAME,
            trade.model_dump(mode="json"),  # 💡 ใส่ mode="json" เพื่อให้แปลง Object Datetime/UUID เป็น String อัตโนมัติ
        )

    def get_trades(self) -> list[dict]:
        return self.get_all(
            self.TABLE_NAME,
        )