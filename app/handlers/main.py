from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.exceptions import CalculationError
from app.methods.encar import get_car_info
from app.models import CarInfo, CarCalculation
from app.states import CalculatorStates
from app.methods import Validator, Formatter, ParseSite, MessageFormatter, GetPrices

router = Router()


@router.message(CalculatorStates.link)
async def link_handler(message: Message, state: FSMContext):
    if not Validator.is_valid_link(message.text):
        await message.answer("Введите корректную ссылку на авто")
        return

    await message.answer("Введите сумму с таблицы")
    await state.update_data(link=message.text)
    await state.set_state(CalculatorStates.sum_from_table)


@router.message(CalculatorStates.sum_from_table)
async def sum_handler(message: Message, state: FSMContext):
    if not Validator.is_valid_value(message.text):
        await message.answer("Неправильное значение!")
        return
    await message.answer("Пожалуйста, подождите...")

    value_from_table: int = Formatter.format_value(message.text)
    car_url: str = await state.get_value('link')
    site = Validator.get_site_name(car_url)
    try:
        car_info: CarInfo = await ParseSite.get_car_info_from_site(car_url) if site == "mdmcar" \
            else await get_car_info(car_url)
    except:
        await message.answer("Произошла ошибка при получении данных об автомобиле.")
        await state.set_state(CalculatorStates.link)
        raise

    try:
        car_calculation: CarCalculation = GetPrices.return_prices(engine_size=car_info['engine_size'],
                                                                  car_year=car_info['year'],
                                                                  car_price=car_info['price'],
                                                                  sum_from_table=value_from_table)
    except Exception as e:
        await message.answer("Произошла ошибка при расчёте.")
        await state.set_state(CalculatorStates.link)
        raise CalculationError(f"An error occurred during the calculation: {e}")

    reply_to_user = MessageFormatter.format_message(car_info=car_info,
                                                    car_calculation=car_calculation,
                                                    car_link=car_url)
    await message.delete()
    await message.answer(text=reply_to_user, disable_web_page_preview=True)
    await state.clear()
    await state.set_state(CalculatorStates.link)
