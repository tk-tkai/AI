import logging
from postgrest.exceptions import APIError
from models.news_item import NewsItemModel
from repositories.base_repository import BaseRepository
from config.supabase_client import get_supabase_client

logger = logging.getLogger("backend.repositories.news_cache_repository")
logger.setLevel(logging.DEBUG)

class NewsCacheRepository(BaseRepository):
    TABLE_NAME: str = "news_cache"

    def __init__(self) -> None:
        super().__init__()
        self.client = get_supabase_client()

    def create_news(self, news: NewsItemModel) -> dict:
        """
        บันทึกข้อมูลข่าวสารลงในตาราง news_cache ของ Supabase
        """
        try:
            data = news.model_dump(mode="json")
            logger.debug("คำขอสำหรับส่งไปบันทึกที่ฐานข้อมูล (Payload): %s", data)

            response = self.client.table(self.TABLE_NAME).insert(data).execute()

            if hasattr(response, "data") and response.data:
                logger.info(
                    "บันทึกข้อมูลลงตาราง '%s' สำเร็จแล้ว! หัวข้อข่าว: '%s'",
                    self.TABLE_NAME,
                    news.title,
                )
                return response.data[0] if isinstance(response.data, list) else response.data

            logger.warning(
                "Supabase ตอบรับคำสั่งสำเร็จแต่ส่งข้อมูลกลับมาว่างเปล่า โปรดตรวจสอบสิทธิ์ RLS ของตาราง ผลลัพธ์: %s",
                response,
            )
            return {}

        except APIError as api_err:
            logger.error(
                "เกิดข้อผิดพลาดจาก Supabase API ในตาราง %s! Code: %s | Message: %s | Details: %s",
                self.TABLE_NAME,
                api_err.code,
                api_err.message,
                getattr(api_err, "details", "None"),
                exc_info=True,
            )
            raise api_err
        except Exception as e:
            logger.error(
                "เกิดข้อผิดพลาดที่ไม่คาดคิดใน NewsCacheRepository.create_news: %s",
                str(e),
                exc_info=True,
            )
            raise e

    def get_news(self) -> list[dict]:
        return self.get_all(self.TABLE_NAME)