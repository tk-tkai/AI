from __future__ import annotations

from config.ai_clients import get_groq_client
from config.logging_config import get_logger
from models.agent_result import AgentResultModel


class SentimentAgent:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.client = get_groq_client()

    def analyze(
        self,
        text: str,
    ) -> AgentResultModel:
        self.logger.info("Running sentiment analysis")

        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Analyze market sentiment and "
                        "respond bullish bearish or neutral."
                    ),
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
        )

        content = completion.choices[0].message.content.lower()

        signal = "HOLD"

        if "bullish" in content:
            signal = "BUY"

        elif "bearish" in content:
            signal = "SELL"

        return AgentResultModel(
            agent="sentiment_agent",
            signal=signal,
            confidence=75,
            reasons=[content[:500]],
        )