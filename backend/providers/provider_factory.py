from providers.base_provider import BaseProvider
from providers.binance_provider import BinanceProvider
from providers.yfinance_provider import YFinanceProvider


class ProviderFactory:
    CRYPTO_SYMBOLS: set[str] = {
        "BTCUSDT",
        "ETHUSDT",
        "SOLUSDT",
    }

    @staticmethod
    def get_provider(
        symbol: str,
    ) -> BaseProvider:
        if symbol in ProviderFactory.CRYPTO_SYMBOLS:
            return BinanceProvider()

        return YFinanceProvider()