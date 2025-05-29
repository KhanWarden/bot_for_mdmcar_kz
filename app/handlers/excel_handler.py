from pathlib import Path

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.states import ExcelHandlerStates

router = Router()
PROJECT_FOLDER = Path(__file__).parent.parent.parent
DATA_FOLDER = Path(PROJECT_FOLDER/"data")
DATA_FOLDER.mkdir(exist_ok=True)


@router.message(Command("loadexcel"))
async def excel_handler(message: Message, state: FSMContext):
    await message.answer("Отправьте таблицу в расширении .xlsx (Excel)")
    await state.set_state(ExcelHandlerStates.excel_file)


@router.message(ExcelHandlerStates.excel_file)
async def excel_file_handler(message: Message, state: FSMContext, bot):
    document = message.document

    if not document.file_name.endswith(".xlsx"):
        await message.reply("Нужен файл с расширением .xlsx")
        return

    try:
        excel_file = await bot.get_file(document.file_id)
        file_path = excel_file.file_path

        local_path = DATA_FOLDER / "excel_file.xlsx"

        await bot.download_file(file_path, destination=str(local_path))
        await message.reply("Файл успешно сохранён!")
        await state.clear()
    except:
        await message.answer("Произошла ошибка при сохранении файла")
        await state.clear()
        raise
