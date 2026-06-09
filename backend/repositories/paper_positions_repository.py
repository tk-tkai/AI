from models.paper_position import PaperPositionModel
from repositories.base_repository import BaseRepository


class PaperPositionsRepository(BaseRepository):
    TABLE_NAME: str = "paper_positions"

    def create_position(
        self,
        position: PaperPositionModel,
    ) -> dict:
        return self.insert(
            self.TABLE_NAME,
            position.model_dump(mode="json"),  # 💡 ปรับเป็น mode="json" เพื่อแปลงฟิลด์ datetime/UUID เป็น String อัตโนมัติ
        )

    def update_position(
        self,
        position_id: str,
        payload: dict,
    ) -> dict:
        return self.update(
            self.TABLE_NAME,
            position_id,
            payload,
        )

    def get_position(
        self,
        position_id: str,
    ) -> dict | None:
        return self.get_by_id(
            self.TABLE_NAME,
            position_id,
        )

    def get_positions(self) -> list[dict]:
        return self.get_all(
            self.TABLE_NAME,
        )