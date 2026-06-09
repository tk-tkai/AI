import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import feedparser
import httpx
from config.settings import get_settings
from models.news_item import NewsItemModel
from services.news_service import NewsService

logger = logging.getLogger("backend.workers.news_worker")
logger.setLevel(logging.DEBUG)


class NewsWorker:

    def __init__(self) -> None:
        self.news_service = NewsService()
        self.settings = get_settings()

        # 1. CryptoCompare Endpoint (JSON API - ฟรีไม่ต้องใช้ Key)
        self.cryptocompare_url = (
            "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
        )

        # 2. CryptoPanic Endpoint (JSON API)
        # หากต้องการใช้ตัวนี้ ให้เพิ่ม CRYPTOPANIC_API_KEY ไว้ในไฟล์ .env แต่ถ้าไม่มี ระบบจะข้ามไปทำงานส่วนอื่นให้โดยอัตโนมัติ
        self.cryptopanic_token = getattr(
            self.settings, "CRYPTOPANIC_API_KEY", ""
        )

        # 3. Yahoo Finance Endpoint (RSS XML Feed - ครอบคลุมข่าว Macro & Crypto)
        self.yahoo_rss_url = "https://finance.yahoo.com/news/rssindex"

    def run(self) -> None:
        logger.info("========================================")
        logger.info("NewsWorker: เริ่มกระบวนการดึงข่าวสารรวมจาก 3 แหล่งข่าวใหญ่")
        logger.info("========================================")
        total_saved = 0

        # --- แหล่งที่ 1: CryptoCompare (JSON API) ---
        total_saved += self._fetch_from_cryptocompare()

        # --- แหล่งที่ 2: CryptoPanic (JSON API) ---
        if self.cryptopanic_token:
            total_saved += self._fetch_from_cryptopanic()
        else:
            logger.info(
                "CryptoPanic: ข้ามการดึงข้อมูลชั่วคราว (เนื่องจากยังไม่มีการตั้งค่า CRYPTOPANIC_API_KEY ในระบบ)"
            )

        # --- แหล่งที่ 3: Yahoo Finance (RSS Feed) ---
        total_saved += self._fetch_from_yahoo_finance()

        logger.info("========================================")
        logger.info(
            "NewsWorker สิ้นสุดการทำงานประจำรอบ | สรุปรวมยอดบันทึกข่าวสารสำเร็จทุกค่าย = %d รายการ",
            total_saved,
        )
        logger.info("========================================")

    def _fetch_from_cryptocompare(self) -> int:
        """ดึงข้อมูลข่าวสารคริปโตผ่าน CryptoCompare API (JSON)"""
        logger.info("กำลังเชื่อมต่อไปยัง: CryptoCompare JSON API...")
        saved_count = 0
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(self.cryptocompare_url)
                if response.status_code != 200:
                    logger.error(
                        "CryptoCompare Error: การเชื่อมต่อล้มเหลวด้วยรหัสสถานะ %d",
                        response.status_code,
                    )
                    return 0

                data = response.json().get("Data", [])
                logger.info(
                    "CryptoCompare: ตรวจพบข่าวสารล่าสุดในระบบจำนวน %d รายการ",
                    len(data),
                )

                for entry in data:
                    try:
                        title = entry.get("title", "").strip()
                        url = entry.get("url", "").strip()
                        summary = entry.get("body", "").strip()
                        source = entry.get("source_info", {}).get(
                            "name", "CryptoCompare"
                        )

                        if not title or not url:
                            continue

                        # แปลง Unix Timestamp เป็น ISO 8601
                        ts = entry.get("published_on")
                        published_at = (
                            datetime.fromtimestamp(
                                int(ts), tz=timezone.utc
                            ).isoformat()
                            if ts
                            else datetime.now(timezone.utc).isoformat()
                        )

                        news_model = NewsItemModel(
                            title=title,
                            summary=summary,
                            source=source,
                            url=url,
                            published_at=published_at,
                        )

                        if self.news_service.save_news(news_model):
                            saved_count += 1
                    except Exception as item_err:
                        logger.debug(
                            "CryptoCompare Item Skipped: %s", str(item_err)
                        )

        except Exception as api_err:
            logger.error("CryptoCompare Service Failure: %s", str(api_err))

        logger.info("-> CryptoCompare: บันทึกสำเร็จ %d รายการ", saved_count)
        return saved_count

    def _fetch_from_cryptopanic(self) -> int:
        """ดึงข้อมูลข่าวสารคริปโตและ Sentiment ผ่าน CryptoPanic API (JSON)"""
        logger.info("กำลังเชื่อมต่อไปยัง: CryptoPanic JSON API...")
        saved_count = 0
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={self.cryptopanic_token}&public=true"
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                if response.status_code != 200:
                    logger.error(
                        "CryptoPanic Error: การเชื่อมต่อล้มเหลวด้วยรหัสสถานะ %d",
                        response.status_code,
                    )
                    return 0

                results = response.json().get("results", [])
                logger.info(
                    "CryptoPanic: ตรวจพบข่าวสารล่าสุดในระบบจำนวน %d รายการ",
                    len(results),
                )

                for entry in results:
                    try:
                        title = entry.get("title", "").strip()
                        url_link = entry.get("url", "").strip()
                        domain = entry.get("domain", "CryptoPanic Source")
                        summary = f"CryptoPanic Sentiment Feed from source domain: {domain}"
                        source = entry.get("source", {}).get(
                            "title", "CryptoPanic"
                        )

                        if not title or not url_link:
                            continue

                        # CryptoPanic ส่งฟอร์แมตเวลาเป็น ISO 8601 อยู่แล้ว
                        published_at = entry.get(
                            "published_at", datetime.now(timezone.utc).isoformat()
                        )

                        news_model = NewsItemModel(
                            title=title,
                            summary=summary,
                            source=source,
                            url=url_link,
                            published_at=published_at,
                        )

                        if self.news_service.save_news(news_model):
                            saved_count += 1
                    except Exception as item_err:
                        logger.debug(
                            "CryptoPanic Item Skipped: %s", str(item_err)
                        )

        except Exception as api_err:
            logger.error("CryptoPanic Service Failure: %s", str(api_err))

        logger.info("-> CryptoPanic: บันทึกสำเร็จ %d รายการ", saved_count)
        return saved_count

    def _fetch_from_yahoo_finance(self) -> int:
        """ดึงข้อมูลข่าวจาก Yahoo Finance (RSS Feed)"""
        logger.info("กำลังเชื่อมต่อไปยัง: Yahoo Finance RSS Feed...")
        saved_count = 0
        try:
            # พรางเบราว์เซอร์เพื่อความสม่ำเสมอในการรับข้อมูล RSS
            feed = feedparser.parse(
                self.yahoo_rss_url,
                agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            )

            entries = feed.get("entries", [])
            logger.info(
                "Yahoo Finance: ตรวจพบข่าวสารล่าสุดในระบบจำนวน %d รายการ",
                len(entries),
            )

            for entry in entries:
                try:
                    title = entry.get("title", "").strip()
                    url_link = entry.get("link", "").strip()
                    summary = entry.get(
                        "summary", entry.get("description", "")
                    ).strip()
                    source = "Yahoo Finance"

                    if not title or not url_link:
                        continue

                    # แปลงเวลาสไตล์ RFC 822 ของ RSS ให้เป็นสไตล์สากล ISO 8601
                    published_str = entry.get(
                        "published", entry.get("pubDate", None)
                    )
                    if published_str:
                        try:
                            published_at = parsedate_to_datetime(
                                published_str
                            ).isoformat()
                        except Exception:
                            published_at = datetime.now(timezone.utc).isoformat()
                    else:
                        published_at = datetime.now(timezone.utc).isoformat()

                    news_model = NewsItemModel(
                        title=title,
                        summary=summary,
                        source=source,
                        url=url_link,
                        published_at=published_at,
                    )

                    if self.news_service.save_news(news_model):
                        saved_count += 1
                except Exception as item_err:
                    logger.debug(
                        "Yahoo Finance Item Skipped: %s", str(item_err)
                    )

        except Exception as api_err:
            logger.error("Yahoo Finance Service Failure: %s", str(api_err))

        logger.info("-> Yahoo Finance: บันทึกสำเร็จ %d รายการ", saved_count)
        return saved_count