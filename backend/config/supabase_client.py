from supabase import Client
from supabase import create_client

from config.settings import get_settings


class SupabaseClientManager:
    def __init__(self) -> None:
        settings = get_settings()

        self._client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY,
        )

    @property
    def client(self) -> Client:
        return self._client


_supabase_manager = SupabaseClientManager()


def get_supabase_client() -> Client:
    return _supabase_manager.client