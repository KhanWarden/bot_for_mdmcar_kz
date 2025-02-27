from app.redis_client import RedisClient
from app.exceptions import RedisError


class CurrencyCache(RedisClient):
    @classmethod
    def get_rate(cls, currency_key: str) -> float:
        try:
            rate = cls.redis.get(currency_key)
            if rate is None:
                raise RedisError(f"Rate for {currency_key} not found")
            return float(rate)
        except Exception as e:
            raise RedisError(f"Error when receiving rate for {currency_key}: {e}")


class ExchangeRates(CurrencyCache):
    """ Exchange Rates of 1$ """
    @classmethod
    def get_kzt_rate(cls) -> float:
        return cls.get_rate('usd_to_kzt_rate')

    @classmethod
    def get_won_rate(cls) -> float:
        return cls.get_rate('usd_to_won_rate')
