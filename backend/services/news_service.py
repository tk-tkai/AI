from config.logging_config import get_logger
from models.news_item import NewsItemModel
from repositories.news_cache_repository import NewsCacheRepository

class NewsService:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.repository = NewsCacheRepository()

    def save_news(self, news: NewsItemModel) -> dict:
        self.logger.info(
            "กำลังเริ่มส่งต่อข้อมูลเข้าสู่ระบบบันทึกข่าวสาร หัวข้อ: '%s'",
            news.title,
        )

        result = self.repository.create_news(news)

        if not result:
            self.logger.error(
                "กระบวนการทำงานเสร็จสิ้น แต่ไม่มีข้อมูลข่าวสารถูกบันทึกลงฐานข้อมูล: '%s'",
                news.title,
            )
        else:
            self.logger.info(
                "กระบวนการทำงานสมบูรณ์ ข้อมูลถูกเขียนและยืนยันแล้วสำหรับ: '%s'",
                news.title,
            )

        return result

    def get_news(self) -> list[dict]:
        return self.repository.get_news()