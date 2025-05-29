import re

from app.exceptions import CarInfoError


def get_car_id_from_link(url: str) -> int:
    if "/cars/detail/" in url:
        try:
            return int(url.split("/cars/detail/")[1].split("?")[0])
        except (IndexError, ValueError):
            pass
    match = re.search(r"carid=(\d+)", url)
    if match:
        return int(match.group(1))



def extract_engine_size(engine_size: str) -> int:
    match = re.search(r"([\d,]+)cc", engine_size)
    if match:
        return int(match.group(1).replace(",", ""))
    raise CarInfoError


def format_engine_type(engine_type: str) -> str:
    engine_types = {
        "가솔린": "Бензиновый",
        "디젤": "Дизельный",
        "가솔린+전기": "Бензиновый + Электрический",
        "디젤+전기": "Дизельный + Электрический",
        "가솔린+LPG": "Бензин + Газ",
        "전기": "Электро",
        "기타": "Другой"
    }
    return engine_types[engine_type]
