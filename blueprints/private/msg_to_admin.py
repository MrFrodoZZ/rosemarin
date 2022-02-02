from vkbottle.bot import Blueprint, Message
from vkbottle import BaseStateGroup


bot = Blueprint('Направление письма администрации')


class MessageToAdmin(BaseStateGroup):

    STATE = 0


@bot.on.private_message(lev='/toadmin')
async def msg_to_admin(message: Message):
    await bot.state_dispenser.set(message.peer_id, MessageToAdmin.STATE)
    return 'Введите ваше обращение к администрации. \
    Всё, что вы сейчас отправите, будет переслано в беседу администрации.'


@bot.on.private_message(state=MessageToAdmin.STATE)
async def send_message(message: Message):
    user = await bot.api.users.get(message.from_id, name_case='gen')
    await bot.api.messages.send(
        peer_id=2000000002,
        message=f'Сообщение от [id{user[0].id}|{user[0].first_name} {user[0].last_name}]:\n\n' + message.text,
        random_id=0)
    await message.answer('Ваше сообщение отправлено администрации.')
