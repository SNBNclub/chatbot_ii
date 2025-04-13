from sqlalchemy import select, desc, distinct, and_

from database.models import User, Dialog, CurDialog, async_session
from errors.errors import *
from handlers.errors import db_error_handler


@db_error_handler
async def get_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))
        if user:
            return user
        else:
            return None


@db_error_handler
async def create_user(tg_id: int):
    async with async_session() as session:
        user = await get_user(tg_id)
        data = {}
        if not user:
            data['id'] = tg_id
            user_data = User(**data)
            session.add(user_data)
            await session.commit()
        else:
            raise Error409


@db_error_handler
async def update_user(tg_id: int, data: dict):
    async with async_session() as session:
        user = await get_user(tg_id)
        if not user:
            raise Error404
        else:
            for key, value in data.items():
                setattr(user, key, value)
            session.add(user)
            await session.commit()


@db_error_handler
async def get_dialog(dialog_id: int):
    async with async_session() as session:
        dialog = await session.scalar(select(Dialog).where(Dialog.id == dialog_id))
        if dialog:
            return dialog
        else:
            return None


@db_error_handler
async def create_dialog(dialog: str):
    async with async_session() as session:
        dialog_data = Dialog(dialog=dialog)
        session.add(dialog_data)
        await session.commit()
        await session.refresh(dialog_data)
        return dialog_data.id


@db_error_handler
async def update_dialog(dialog_id: int, dialog: str):
    async with async_session() as session:
        dialog_row = await get_dialog(dialog_id)
        if not dialog_row:
            raise Error404
        else:
            setattr(dialog_row, 'dialog', dialog)
            session.add(dialog_row)
            await session.commit()


@db_error_handler
async def get_cur_dialog(tg_id: int):
    async with async_session() as session:
        cur_dialog = await session.scalar(select(CurDialog).where(CurDialog.user_id == tg_id))
        if cur_dialog:
            return cur_dialog
        else:
            return None


@db_error_handler
async def add_cur_dialog(tg_id: int, dialog_id: int):
    async with async_session() as session:
        cur_dialog = await get_cur_dialog(tg_id)
        if not cur_dialog:
            data = {'user_id': tg_id, 'dialog_id': dialog_id}
            cur_dialog_data = CurDialog(**data)
            session.add(cur_dialog_data)
            await session.commit()
        else:
            raise Error409


@db_error_handler
async def delete_cur_dialog(tg_id: int):
    async with async_session() as session:
        cur_dialog = await get_cur_dialog(tg_id)
        if cur_dialog:
            await session.delete(cur_dialog)
            await session.commit()
        else:
            raise Error404
