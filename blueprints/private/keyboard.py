from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, \
                        OpenLink, EMPTY_KEYBOARD
import config as cfg


bot = Blueprint('Клавиатура')


@bot.on.private_message(text=['/start', '/menu'])
async def start(message: Message):
    keyboard = (
        Keyboard(one_time=True)
        .add(Text('/rules'), color=KeyboardButtonColor.PRIMARY)
        .add(Text('/char'))
        .add(Text('/toadmin'))
    )
    await message.answer(cfg.cmd_list, keyboard=keyboard)


@bot.on.private_message(text=['/rules'])
async def rules_keyboard(message: Message):
    keyboard = (
        Keyboard(one_time=True)
        .add(Text('/rules 0'), color=KeyboardButtonColor.PRIMARY)
        .add(Text('/rules 1'))
        .add(Text('/rules 2'))
        .add(Text('/rules 3'))
        .add(Text('/rules 4'))
    )
    await message.answer(cfg.rules_noarg, keyboard=keyboard)
