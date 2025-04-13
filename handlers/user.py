from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from handlers.errors import safe_send_message
from keyboards.keyboards import get_cancel_ikb, get_restart_ikb
from instance import bot
from database.req import *
from assistant.handlers import *

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await create_user(message.from_user.id)
    await safe_send_message(bot, message, text="Привет, что бы я тебе помог напиши /help")


@router.message(Command('info'))
async def cmd_info(message: Message):
    await safe_send_message(bot, message, text="Какая-то информация")


class DialogState(StatesGroup):
    start_dialog = State()


@router.message(Command('help'))
async def start_dialog(message: Message, state: FSMContext):
    cur_dialog = await get_cur_dialog(message.from_user.id)
    if cur_dialog:
        await safe_send_message(bot, message, "У вас есть активный диалог, хотите его продолжить?",
                                reply_markup=get_restart_ikb())
        return
    cur_dialog = await create_assistant_dialog()
    await add_cur_dialog(message.from_user.id, cur_dialog)
    msg = await assistant_message(cur_dialog, 'начни диалог')
    await safe_send_message(bot, message, msg, reply_markup=get_cancel_ikb())
    await state.set_data({'cur_dialog': cur_dialog})
    await state.set_state(DialogState.start_dialog)


@router.message(DialogState.start_dialog)
async def cont_dialog(message: Message, state: FSMContext):
    cur_dialog = (await state.get_data()).get('cur_dialog', None)
    if not cur_dialog:
        await safe_send_message(bot, message, 'У вас нет тенущего дилога')
        await state.clear()
        return
    msg = await assistant_message(cur_dialog, message.text)
    await safe_send_message(bot, message, msg, reply_markup=get_cancel_ikb())


@router.callback_query(lambda c: c.data and c.data.startswith("dialog"))
async def restart(callback: CallbackQuery, state: FSMContext):
    reply = callback.data.split(":")[1]
    if reply == 'cont':
        cur_dialog = (await get_cur_dialog(callback.from_user.id)).id
        msg = await assistant_message(cur_dialog, 'продолжи этот диалог')
        await callback.answer()
        await safe_send_message(bot, callback, msg, reply_markup=get_cancel_ikb())
        await state.set_data({'cur_dialog': cur_dialog})
        await state.set_state(DialogState.start_dialog)
    elif reply == 'restart':
        cur_dialog = await create_assistant_dialog()
        await add_cur_dialog(callback.from_user.id, cur_dialog)
        msg = await assistant_message(cur_dialog, 'начни диалог')
        await callback.answer()
        await safe_send_message(bot, callback, msg, reply_markup=get_cancel_ikb())
        await state.set_data({'cur_dialog': cur_dialog})
        await state.set_state(DialogState.start_dialog)


@router.callback_query(lambda c: c.data and c.data.startswith("end"))
async def end_dailof(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await safe_send_message(bot, callback, "Диалог закончен")
    await delete_cur_dialog(callback.from_user.id)
    await state.clear()
