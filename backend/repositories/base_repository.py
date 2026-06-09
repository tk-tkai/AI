from abc import ABC
from typing import Any

from supabase import Client

from config.logging_config import get_logger
from config.supabase_client import get_supabase_client


class BaseRepository(ABC):
    def __init__(self) -> None:
        self.client: Client = get_supabase_client()
        self.logger = get_logger(self.__class__.__name__)

    def insert(self, table_name: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.logger.info("Insert into table=%s", table_name)

        response = (
            self.client.table(table_name)
            .insert(payload)
            .execute()
        )

        return {
            "data": response.data
        }

    def update(
        self,
        table_name: str,
        record_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        self.logger.info(
            "Update table=%s id=%s",
            table_name,
            record_id,
        )

        response = (
            self.client.table(table_name)
            .update(payload)
            .eq("id", record_id)
            .execute()
        )

        return {
            "data": response.data
        }

    def delete(
        self,
        table_name: str,
        record_id: str,
    ) -> dict[str, Any]:
        self.logger.warning(
            "Delete table=%s id=%s",
            table_name,
            record_id,
        )

        response = (
            self.client.table(table_name)
            .delete()
            .eq("id", record_id)
            .execute()
        )

        return {
            "data": response.data
        }

    def get_by_id(
        self,
        table_name: str,
        record_id: str,
    ) -> dict[str, Any] | None:
        self.logger.info(
            "Get table=%s id=%s",
            table_name,
            record_id,
        )

        response = (
            self.client.table(table_name)
            .select("*")
            .eq("id", record_id)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    def get_all(
        self,
        table_name: str,
    ) -> list[dict[str, Any]]:
        self.logger.info(
            "Get all from table=%s",
            table_name,
        )

        response = (
            self.client.table(table_name)
            .select("*")
            .execute()
        )

        return response.data