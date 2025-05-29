from datetime import datetime

import pytz

from app.methods import ExchangeRates, Formatter
from app.models import CarCalculation, CarInfo


class MessageFormatter:
    TEMPLATE = """
🔸 {total_price_kz} тг • Стоимость под ключ Алматы
🔸 {transit_total} тг • Стоимость на транзитах

▫️ {car_name}
▫️ {mileage} км.
▫️ {engine_size} см³
▫️ {engine_type}
▫️ {manufacture_date}
Посмотреть автомобиль
{car_link}
———————————————
🔹 {broker_fee} тг + {customs_fee} тг • Услуги брокера + Таможня
(Сертификат СКБТС, ЕПТС, Доверенность, СВХ)
🔹 {recycling_fee} тг • Утилизационный сбор
🔹 {first_registration_fee} тг • Первичная регистрация
Курс $1 = ₩ {krw_rate} / ₸ {kzt_rate}
———————————————
🔻 ВАЖНО! {date}-{time}:{price_short}
• Стоимость автомобиля и услуги могут меняться от курса валют на дату оплаты
• Расчет таможни может меняться от курса доллара
———————————————
"""

    @classmethod
    def format_message(cls, car_info: CarInfo, car_calculation: CarCalculation, car_link: str) -> str:
        kzt, won = cls._get_exchange_rates()

        moscow_datetime = cls._get_moscow_tz()
        _time = moscow_datetime.strftime("%H:%M:%S")
        _date = moscow_datetime.strftime("%d.%m.%y")

        kwargs = {
            "krw_rate": won,
            "kzt_rate": kzt,

            "total_price_kz": Formatter.format_number_with_spaces(car_calculation['total']),
            "transit_price_kz": Formatter.format_number_with_spaces(car_calculation['transit']),
            "broker_fee": Formatter.format_number_with_spaces(car_calculation['static_expenses']),
            "customs_fee": Formatter.format_number_with_spaces(car_calculation['customs']),
            "recycling_fee": Formatter.format_number_with_spaces(car_calculation['recycling_fee']),
            "first_registration_fee": Formatter.format_number_with_spaces(car_calculation['first_registration_fee']),

            "car_name": car_info['car_name'],
            "mileage": Formatter.format_number_with_spaces(car_info['mileage']),
            "engine_size": Formatter.format_number_with_spaces(car_info['engine_size']),
            "engine_type": car_info['engine_type'],
            "manufacture_date": f"{Formatter.format_month(car_info['month'])}.{car_info['year']}",
            "car_link": car_link,

            "transit_total": Formatter.format_number_with_spaces(car_calculation['transit']
                                                                 + car_calculation['static_expenses']
                                                                 + car_calculation['customs']),
            "date": _date,
            "time": _time,
            "price_short": car_info['price'],
        }
        try:
            return cls.TEMPLATE.format(**kwargs)
        except CarCalculation:
            print("Error while car calculating")

    @classmethod
    def _get_exchange_rates(cls) -> tuple[float, float]:
        kzt = ExchangeRates.get_kzt_rate()
        won = ExchangeRates.get_won_rate()
        return kzt, won

    @classmethod
    def _get_moscow_tz(cls) -> datetime:
        moscow_tz = pytz.timezone("Europe/Moscow")
        moscow_now = datetime.now(moscow_tz)
        return moscow_now
