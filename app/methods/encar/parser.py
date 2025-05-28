from typing import Any, Dict

import aiohttp

from .utils import format_engine_type, get_car_id_from_link
from app.models import CarInfo


BASE_URL = f"https://api.encar.com/v1/readside/vehicle/"


async def get_car_info(url: str) -> CarInfo:
    car_id = get_car_id_from_link(url)
    car_info = await _parse_page(car_id)
    return car_info


async def _get_json(car_id: int) -> Dict[Any, Any]:
    async with aiohttp.ClientSession() as session:
        request = await session.get(f"{BASE_URL}/{car_id}")
        json = await request.json()
        return json


async def _parse_page(car_id: int) -> CarInfo:
    json_: dict = await _get_json(car_id)
    vehicle_id = int(json_.get("vehicleId"))
    car_name = (json_.get("category").get("manufacturerEnglishName", "") + " " + json_.get("category").get(
        "modelGroupEnglishName", "") + " " + json_.get("category").get("gradeEnglishName", "")).strip()

    price: int = int(json_.get("advertisement").get("price"))

    mileage = int(json_.get("spec").get("mileage"))

    engine_type = format_engine_type(json_.get("spec").get("fuelName"))
    engine_size = json_.get("spec").get("displacement")

    year_month = json_.get("category").get("yearMonth")
    year, month = int(year_month[:4]), int(year_month[4:])

    photos = json_.get("photos")
    photo_link = [f"https://ci.encar.com{photo["path"]}" for photo in photos if photo["path"].endswith("001.jpg")][0]

    kwargs = {
        "vehicle_id": vehicle_id,
        "car_name": car_name,
        "price": price,
        "engine_size": engine_size,
        "engine_type": engine_type,
        "mileage": mileage,
        "year": year,
        "month": month,
        "photo_link": photo_link
    }
    return CarInfo(**kwargs)
