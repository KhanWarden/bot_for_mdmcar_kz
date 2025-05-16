from aiogram.fsm.state import StatesGroup, State


class CalculatorStates(StatesGroup):
    sum_from_table = State()
    link = State()
