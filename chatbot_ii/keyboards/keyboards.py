from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_cancel_ikb() -> InlineKeyboardMarkup:
    ikb = [
        [InlineKeyboardButton(text="Закончить диалог", callback_data="end_dialog")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard


def get_restart_ikb() -> InlineKeyboardMarkup:
    ikb = [
        [InlineKeyboardButton(text="Продолжить", callback_data="dialog:cont"),
         InlineKeyboardButton(text="Начать новый", callback_data="dialog:restart")],
    ]
    ikeyboard = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ikeyboard
