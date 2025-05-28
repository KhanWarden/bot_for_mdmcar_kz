from pathlib import Path
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("car_price_lookup")

PROJECT_FOLDER = Path(__file__).parent.parent.parent
DATA_FOLDER = PROJECT_FOLDER / "data"
xls = DATA_FOLDER / "excel_file.xlsx"

df = pd.read_excel(
    xls,
    sheet_name="База",
    usecols="A:E",
    header=None,
    names=["brand", "model", "engine", "year", "price"]
)
df.dropna(subset=["brand", "model", "engine", "year", "price"], inplace=True)
df["brand"] = df["brand"].astype(str).str.strip().str.upper()
df["model"] = df["model"].astype(str).str.strip().str.upper()


def normalize(text: str) -> str:
    return text.replace(" ", "").upper()


def model_matches(input_model: str, table_model: str) -> bool:
    return normalize(table_model) in normalize(input_model)


def split_brand_model(full_name: str, brand_list: list[str]) -> tuple[str, str]:
    full_name = full_name.strip().upper()
    for brand in sorted(brand_list, key=len, reverse=True):
        if full_name.startswith(brand):
            model = full_name[len(brand):].strip()
            return brand, model
    raise ValueError(f"Не удалось определить бренд в '{full_name}'")


def get_car_price(full_name: str, engine: float, year: int) -> int:
    try:
        brand_list = df["brand"].unique().tolist()
        brand, model = split_brand_model(full_name, brand_list)

        df_filtered = df[
            (df["brand"] == brand) &
            (df["model"].apply(lambda m: model_matches(model, m)))
        ]

        if df_filtered.empty:
            logger.error(f"Автомобиль '{full_name}' не найден")
            raise ValueError(f"Автомобиль '{full_name}' не найден")

        df_year = df_filtered[df_filtered["year"] == year]
        max_available_year = None
        if df_year.empty:
            max_available_year = df_filtered["year"].max()
            df_year = df_filtered[df_filtered["year"] == max_available_year]
            apply_depreciation = True
        else:
            apply_depreciation = False

        volumes = df_year["engine"].dropna().unique()
        if len(volumes) == 0:
            logger.error(f"Нет объёма двигателя для '{full_name}' {year}")
            raise ValueError(f"Нет данных по объёму двигателя")

        nearest_volume = volumes[np.argmin(np.abs(volumes - engine))]
        row = df_year[df_year["engine"] == nearest_volume]

        if row.empty:
            logger.error(f"Не найдена цена для '{full_name}' {year} с объёмом {nearest_volume}")
            raise ValueError(f"Нет цены для '{full_name}' {year} с объёмом {nearest_volume}")

        base_price = int(row.iloc[0]["price"])

        if not apply_depreciation:
            return base_price

        year_diff = int(max_available_year - year)
        for _ in range(year_diff):
            base_price *= 0.85
        return int(base_price)

    except Exception as e:
        logger.exception("Ошибка при поиске цены автомобиля")
        raise
