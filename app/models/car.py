from typing import TypedDict


class CarInfo(TypedDict):
    car_name: str
    price: int
    engine_size: int
    engine_type: str
    mileage: int
    year: int
    month: int
    photo_link: str


class CarCalculation(TypedDict):
    transit: int
    recycling_fee: int
    first_registration_fee: int
    static_expenses: int
    customs: int
    total: int
