from gigachat.models import Chat, Messages, MessagesRole

from database.req import create_dialog, get_dialog, update_dialog
from instance import GC


async def create_assistant_dialog() -> int:
    payload = Chat(
        messages=[
            Messages(
                role=MessagesRole.SYSTEM,
                content="Ты внимательный бот-психолог, который помогает пользователю решить его проблемы."
            )
        ],
    )
    dialog_id = await create_dialog(payload.json())
    return dialog_id


async def assistant_message(dialog_id: int, mes: str) -> str:
    dialog = await get_dialog(dialog_id)
    payload = Chat.parse_raw(dialog.dialog)
    async with GC as giga:
        payload.messages.append(Messages(role=MessagesRole.USER, content=mes))
        response = giga.chat(payload)
        payload.messages.append(response.choices[0].message)
        await update_dialog(dialog_id, payload.json())
        return response.choices[0].message.content
