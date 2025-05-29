import json
import re

import aiohttp

from app.exceptions import InvalidCarId
from .currency_cache import ExchangeRates
from app.models import CarInfo


class MDMCarUtils:
    @classmethod
    def extract_car_id(cls, url: str) -> int:
        pattern = r"car/(\d+)"
        match = re.search(pattern, url)
        if match:
            return int(match.group(1))
        else:
            raise InvalidCarId(f"{url}: Ошибка, ID не найден")

    @classmethod
    def format_engine_type(cls, engine_type: int) -> str:
        engine_types = {
            1: "Бензиновый",
            2: "Дизельный",
            3: "Газ",
            4: "Гибрид",
            5: "Электро"
        }
        return engine_types[engine_type]

    @classmethod
    def format_car_info(cls, data: dict) -> CarInfo:
        car_info = data["car"]

        car_brand: str = data["manufacturer"]["name"]
        car_model: str = data["model"]["name"]
        car_badge: str = car_info["badge"]
        car_badge_detail: str | None = car_info.get("badge_detail", "")

        car_name = f"{car_brand} {car_model} {car_badge} {car_badge_detail}".strip()

        photo_name: str = car_info["main_photo"]
        photo_link_template: str = "https://media.mdmcar.com/static/"
        photo_link: str = f"{photo_link_template}/{photo_name[:2]}/{photo_name[2:4]}/{photo_name[4:6]}/{photo_name[6:8]}/{photo_name}"

        engine_type = cls.format_engine_type(car_info["fuel_type"])

        kwargs = {
            "car_name": car_name,
            "price": car_info["price"],
            "engine_size": car_info["engine"],
            "engine_type": engine_type,
            "mileage": car_info["mileage"],
            "year": car_info["year"],
            "month": car_info["month"],
            "photo_link": photo_link
        }
        return CarInfo(**kwargs)


class ParseSite(MDMCarUtils):
    @classmethod
    async def get_car_info_from_site(cls, url: str) -> CarInfo:
        car_id: int = cls.extract_car_id(url)
        request_url: str = f"https://mdmcar.com:2096/api/car/getCar?id={car_id}"

        data: dict = await cls.fetch_json(request_url)
        car_info: CarInfo = cls.format_car_info(data)

        for key, value in car_info.items():
            if not value:
                raise TypeError("There is None in dictionary")

        return car_info

    @classmethod
    async def fetch_json(cls, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as resp:
                    if resp.status != 200:
                        raise Exception(f"Ошибка запроса: {resp.status}")
                    text: str = await resp.text()
                    data: dict = json.loads(text)

                    return data
            except Exception as e:
                print(f"Произошла ошибка: {e}")
