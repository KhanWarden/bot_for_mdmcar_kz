from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .main import router as calc_router
from ..states import CalculatorStates

router = Router()
router.include_routers(calc_router)


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()

    if message.chat.type != 'private':
        await message.answer("Бот работает только в лс!")
        return

    await message.answer(text="Вас приветствует электронный помощник компании <b>MDMCAR_KOREA</b>!\n"
                              "С моей помощью Вы можете из Южной Кореи просчитать все необходимые расходы.\n"
                              "Вставьте ссылку с нашего сайта (mdmcar.com/)",
                         disable_web_page_preview=True,
                         )
    await state.set_state(CalculatorStates.link)
