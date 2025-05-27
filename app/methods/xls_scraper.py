from pathlib import Path

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("car_price_lookup")

PROJECT_FOLDER = Path(__file__).parent.parent.parent
DATA_FOLDER = PROJECT_FOLDER / "data"


xls = DATA_FOLDER / "excel_file.xlsx"
df = pd.read_excel(xls, sheet_name="База", usecols="A:E", names=["brand", "model", "engine", "year", "price"])
df.dropna(subset=["brand", "model", "engine", "year", "price"], inplace=True)
df["brand"] = df["brand"].astype(str).str.strip().str.upper()
df["model"] = df["model"].astype(str).str.strip().str.upper()


def get_car_price(full_name: str, engine: float, year: int) -> int:
    try:
        brand_list = df["brand"].dropna().astype(str).str.upper().unique().tolist()
        brand, model = split_brand_model(full_name, brand_list)

        df_filtered = df[
            (df["brand"] == brand) &
            (df["model"].apply(lambda m: model.startswith(m)))
            ]
        if df_filtered.empty:
            logger.error(f"Автомобиль '{full_name}' не найден в таблице")
            raise ValueError(f"Автомобиль '{full_name}' не найден")

        df_year = df_filtered[df_filtered["year"] == year]
        if df_year.empty:
            logger.error(f"Год {year} не найден для '{full_name}'")
            raise ValueError(f"Год {year} не найден для '{full_name}'")

        volumes = df_year["engine"].dropna().unique()
        if len(volumes) == 0:
            logger.error(f"Нет объёма двигателя для '{full_name}' {year}")
            raise ValueError(f"Нет данных по объёму двигателя")

        nearest_volume = volumes[np.argmin(np.abs(volumes - engine))]
        row = df_year[df_year["engine"] == nearest_volume]

        if row.empty:
            logger.error(f"Не найдена цена для '{full_name}' {year} с объёмом {nearest_volume}")
            raise ValueError(f"Нет цены для автомобиля '{full_name}' {year}")

        return int(row.iloc[0]["price"])

    except Exception as e:
        logger.exception("Ошибка при поиске цены автомобиля")
        raise


def split_brand_model(full_name: str, brand_list: list[str]) -> tuple[str, str]:
    full_name = full_name.strip().upper()
    for brand in sorted(brand_list, key=len, reverse=True):
        if full_name.startswith(brand):
            model = full_name[len(brand):].strip()
            return brand, model
    raise ValueError(f"Не удалось определить бренд в '{full_name}'")
