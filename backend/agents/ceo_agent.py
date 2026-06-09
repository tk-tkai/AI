from __future__ import annotations

import json

from config.ai_clients import get_groq_client
from config.logging_config import get_logger
from models.agent_result import AgentResultModel
from models.ceo_decision import CEODecisionModel


class CEOAgent:
    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)
        self.client = get_groq_client()

    def decide(
        self,
        chart_result: AgentResultModel,
        news_result: AgentResultModel,
        sentiment_result: AgentResultModel,
        entry: float,
    ) -> CEODecisionModel:
        self.logger.info("Generating final decision based on sub-agents")

        payload = {
            "chart": chart_result.model_dump(),
            "news": news_result.model_dump(),
            "sentiment": sentiment_result.model_dump(),
        }

        # 💡 ล็อกเงื่อนไข JSON Output ของ Llama 3.3 อย่างเข้มงวด
        system_prompt = (
            "You are a Executive CEO trading agent. Your job is to aggregate the analysis "
            "from the Chart Agent, News Agent, and Sentiment Agent to make the definitive trading decision.\n\n"
            "You must return a JSON object with exactly the following keys:\n"
            "1. 'final_signal': strictly choose one from ['BUY', 'SELL', 'HOLD'] (Must be UPPERCASE).\n"
            "2. 'confidence': an integer rating from 0 to 100 based on the consensus of your agents."
        )

        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": json.dumps(payload),
                },
            ],
        )

        try:
            result = json.loads(completion.choices[0].message.content)
            # ป้องกันกรณี LLM พ่นตัวพิมพ์เล็ก ให้ Force เป็นตัวพิมพ์ใหญ่ทั้งหมด
            final_signal = str(result.get("final_signal", "HOLD")).upper()
            confidence = int(result.get("confidence", 0))

            if final_signal not in ["BUY", "SELL", "HOLD"]:
                final_signal = "HOLD"
        except Exception as exc:
            # หากระบบ JSON มีปัญหา ให้ Fallback กลับมาที่ HOLD แทนการปล่อยให้บอทพัง
            self.logger.error("Failed to parse CEO decision JSON, falling back to HOLD. Error: %s", str(exc))
            final_signal = "HOLD"
            confidence = 0

        return CEODecisionModel(
            final_signal=final_signal,
            confidence=confidence,
            entry=entry,
            sl=None,  # สอดคล้องกับโมเดลใหม่ที่ยอมรับค่า None
            tp=None,
        )