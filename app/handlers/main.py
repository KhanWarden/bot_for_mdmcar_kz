from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.exceptions import VehicleNotFoundError
from app.handlers.methods import process_and_respond
from app.methods.encar import get_car_info
from app.methods.xls_scraper import get_car_price
from app.models import CarInfo
from app.states import CalculatorStates
from app.methods import Validator, Formatter, ParseSite

router = Router()


@router.message(CalculatorStates.link)
async def link_handler(message: Message, state: FSMContext):
    if not Validator.is_valid_link(message.text):
        await message.answer("Введите корректную ссылку на авто")
        return

    car_url = message.text
    site = Validator.get_site_name(car_url)
    try:
        car_info: CarInfo = await ParseSite.get_car_info_from_site(car_url) if site == "mdmcar" \
            else await get_car_info(car_url)
    except:
        await message.answer("Произошла ошибка при получении данных об автомобиле.")
        await state.set_state(CalculatorStates.link)
        return

    try:
        value_from_table = get_car_price(full_name=car_info.get("car_name"),
                                         engine=car_info.get("engine_size"),
                                         year=car_info.get("year"), )
    except (VehicleNotFoundError, Exception):
        await message.answer("В каталоге нет этого автомобиля.\n"
                             "Введите сумму")
        await state.update_data(car_info=car_info, car_url=car_url)
        await state.set_state(CalculatorStates.sum_from_table)
        return

    await process_and_respond(message, state, car_info, car_url, value_from_table)


@router.message(CalculatorStates.sum_from_table)
async def sum_handler(message: Message, state: FSMContext):
    if not Validator.is_valid_value(message.text):
        await message.answer("Введите корректное число")
        return

    sum_from_table: int = Formatter.format_value(message.text)
    car_info: CarInfo = await state.get_value("car_info")
    car_url: str = await state.get_value("car_url")

    await process_and_respond(message, state, car_info, car_url, sum_from_table)
