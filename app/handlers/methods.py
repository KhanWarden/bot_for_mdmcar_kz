from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.methods import GetPrices, MessageFormatter
from app.models import CarInfo, CarCalculation
from app.states import CalculatorStates


async def process_and_respond(message: Message, state: FSMContext,
                              car_info: CarInfo, car_url: str, sum_from_table: int):
    try:
        car_calculation: CarCalculation = GetPrices.return_prices(
            engine_size=car_info['engine_size'],
            car_year=car_info['year'],
            car_price=car_info['price'],
            sum_from_table=sum_from_table
        )
    except Exception as e:
        await message.answer("Произошла ошибка при расчёте.")
        await state.set_state(CalculatorStates.link)
        return

    reply_to_user = MessageFormatter.format_message(
        car_info=car_info,
        car_calculation=car_calculation,
        car_link=car_url
    )

    await message.answer(text=reply_to_user, disable_web_page_preview=True)
    await state.clear()
    await state.set_state(CalculatorStates.link)
