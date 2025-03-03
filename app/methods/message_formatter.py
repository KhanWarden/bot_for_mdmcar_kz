from app.methods import ExchangeRates, Formatter
from app.models import CarCalculation, CarInfo


class MessageFormatter:
    TEMPLATE = """
🔸 {total_price_kz} тг • Стоимость под ключ Алматы
🔸 {transit_price_kz} тг • Стоимость на транзитах

▫️ {car_name}
▫️ {mileage} км.
▫️ {engine_size} см³
▫️ {engine_type}
▫️ {manufacture_date}
———————————————
Курс $1 = ₩ {krw_rate}
Курс $1 = ₸ {kzt_rate}

Посмотреть автомобиль
{car_link}

🔻 ВАЖНО!
• Стоимость автомобиля и услуги могут меняться от курса валют на дату оплаты
• Расчет таможни может меняться от курса доллара
———————————————
———————————————
🔹 {broker_fee} тг + {customs_fee} тг • Услуги брокера + Таможня
(Сертификат СКБТС, ЕПТС, Доверенность, СВХ)
🔹 {recycling_fee} тг • Утилизационный сбор
🔹 {first_registration_fee} тг • Первичная регистрация
"""

    @classmethod
    def format_message(cls, car_info: CarInfo, car_calculation: CarCalculation, car_link: str) -> str:
        kzt, won = cls._get_exchange_rates()

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
        }

        return cls.TEMPLATE.format(**kwargs)

    @classmethod
    def _get_exchange_rates(cls) -> tuple[float, float]:
        kzt = ExchangeRates.get_kzt_rate()
        won = ExchangeRates.get_won_rate()
        return kzt, won
