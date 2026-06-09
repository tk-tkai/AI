from groq import Groq

from config.settings import get_settings


class GroqClientManager:
    def __init__(self) -> None:
        settings = get_settings()

        self._client = Groq(
            api_key=settings.GROQ_API_KEY,
        )

    @property
    def client(self) -> Groq:
        return self._client


_groq_manager = GroqClientManager()


def get_groq_client() -> Groq:
    return _groq_manager.client