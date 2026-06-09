from __future__ import annotations

from config.ai_clients import get_groq_client
from config.logging_config import get_logger
from models.agent_result import AgentResultModel


class NewsAgent:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.client = get_groq_client()

    def analyze(
        self,
        news_text: str,
    ) -> AgentResultModel:
        self.logger.info("Running news analysis")

        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Analyze financial news. "
                        "Return BUY SELL or HOLD."
                    ),
                },
                {
                    "role": "user",
                    "content": news_text,
                },
            ],
        )

        content = completion.choices[0].message.content.upper()

        signal = "HOLD"

        if "BUY" in content:
            signal = "BUY"

        elif "SELL" in content:
            signal = "SELL"

        return AgentResultModel(
            agent="news_agent",
            signal=signal,
            confidence=70,
            reasons=[content[:500]],
        )