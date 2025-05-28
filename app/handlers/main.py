from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.exceptions import CalculationError
from app.methods.encar import get_car_info
from app.methods.xls_scraper import get_car_price
from app.models import CarInfo, CarCalculation
from app.states import CalculatorStates
from app.methods import Validator, Formatter, ParseSite, MessageFormatter, GetPrices

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
    except:
        await message.answer("Произошла ошибка при получении суммы с таблицы")
        return

    try:
        car_calculation: CarCalculation = GetPrices.return_prices(engine_size=car_info['engine_size'],
                                                                  car_year=car_info['year'],
                                                                  car_price=car_info['price'],
                                                                  sum_from_table=value_from_table)
    except Exception as e:
        await message.answer("Произошла ошибка при расчёте.")
        await state.set_state(CalculatorStates.link)
        return

    reply_to_user = MessageFormatter.format_message(car_info=car_info,
                                                    car_calculation=car_calculation,
                                                    car_link=car_url)
    await message.answer(text=reply_to_user, disable_web_page_preview=True)
    await state.clear()
    await state.set_state(CalculatorStates.link)
