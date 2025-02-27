from datetime import datetime

from app.models import CarCalculation
from .currency_cache import ExchangeRates


class Calculator:
    KZT: float = ExchangeRates.get_kzt_rate()

    @classmethod
    def calculate(cls, engine_size: int, car_year: int, sum_from_table: int, car_price: int) -> int:
        transit = cls._calculate_transit(car_price)
        customs = cls._calculate_customs_and_static(sum_from_table)
        kz_fees = cls._calculate_kazakhstan_fees(car_year=car_year, engine_size=engine_size)

        total = transit + customs + kz_fees

        return total

    @classmethod
    def _calculate_transit(cls, car_price: int) -> int:
        logistics: int = 2200  # USD
        commission: int = 750  # USD
        return int((logistics + commission + car_price) * cls.KZT)

    @classmethod
    def _calculate_customs(cls, sum_from_table: int) -> int:
        customs_duty: float = 23600 / cls.KZT  # Таможенный сбор (в долларах)
        customs_fee: float = sum_from_table * 0.15  # Таможенная пошлина (в долларах)
        vat: float = (sum_from_table + customs_duty + customs_fee) * 0.12  # НДС (в долларах)

        customs_expenses_in_kzt: int = int(cls._convert_usd_to_kzt(customs_duty, customs_fee, vat))

        return customs_expenses_in_kzt

    @classmethod
    def _calculate_customs_and_static(cls, sum_from_table: int) -> int:
        static_expenses: int = 420000
        customs_expenses_in_kzt: int = cls._calculate_customs(sum_from_table)
        return int(static_expenses + customs_expenses_in_kzt)

    @classmethod
    def _calculate_kazakhstan_fees(cls, car_year: int, engine_size: int) -> int:
        recycling_fee: int = RecyclingFee.calculate(engine_size)
        first_registration_fee: int = FirstRegistrationFee.calculate(car_year)

        return first_registration_fee + recycling_fee

    @classmethod
    def _convert_usd_to_kzt(cls, *args: float) -> float:
        total_usd = sum(args)
        return total_usd * cls.KZT


class RecyclingFee:
    RATES = {
        (0, 1000): 294900,
        (1000, 2000): 688100,
        (2000, 3000): 983000,
        (3000, float("inf")): 2260900
    }

    @classmethod
    def calculate(cls, engine_size: int) -> int:
        for (min_vol, max_vol), price in cls.RATES.items():
            if min_vol < engine_size <= max_vol:
                return price
        return 0


class FirstRegistrationFee:
    current_year = datetime.now().year

    @classmethod
    def calculate(cls, car_year: int) -> int:
        if (cls.current_year - 3) < car_year < cls.current_year:
            return 196600
        elif car_year == cls.current_year:
            return 983
        return 1966000


class GetPrices(Calculator):
    @classmethod
    def return_prices(cls, engine_size: int, car_year: int, sum_from_table: int, car_price: int) -> CarCalculation:
        kwargs = {
            "transit": cls._calculate_transit(car_price),
            "recycling_fee": RecyclingFee.calculate(engine_size),
            "first_registration_fee": FirstRegistrationFee.calculate(car_year),
            "static_expenses": 420000,
            "customs": cls._calculate_customs(sum_from_table),
            "total": cls.calculate(engine_size, car_year, sum_from_table, car_price)
        }
        return CarCalculation(**kwargs)
