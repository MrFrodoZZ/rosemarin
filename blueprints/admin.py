from vkbottle.bot import Blueprint, Message
from vkbottle import CtxStorage, BaseStateGroup
import sqlite3
import config as cfg


bot = Blueprint('Админские команды')
ctx = CtxStorage()
db = sqlite3.connect(cfg.database)
sql = db.cursor()


class AddCharData(BaseStateGroup):
    NAME = 0
    BLANK = 1
    COUNT = 2
    OWNER = 3


@bot.on.message(text='/get.peerid')
async def get_peer_id(message: Message):
    print(message.peer_id)
    await message.answer('PEER_ID вынесен в консоль')


@bot.on.private_message(lev='/addchar')
async def add_char1(message: Message):
    await bot.state_dispenser.set(message.peer_id, AddCharData.NAME)
    return 'Введите имя персонажа:'


@bot.on.private_message(state=AddCharData.NAME)
async def name_handler(message: Message):
    ctx.set('name', message.text)
    await bot.state_dispenser.set(message.peer_id, AddCharData.BLANK)
    return 'Укажите ID ПЕРВОГО сообщения анкеты в обсуждении:'


@bot.on.private_message(state=AddCharData.BLANK)
async def blank_id_handler(message: Message):
    ctx.set('blank_id', message.text)
    await bot.state_dispenser.set(message.peer_id, AddCharData.COUNT)
    return 'Укажите кол-во сообщений анкеты в обсуждении:'


@bot.on.private_message(state=AddCharData.COUNT)
async def blank_count_handler(message: Message):
    ctx.set('blank_count', message.text)
    await bot.state_dispenser.set(message.peer_id, AddCharData.OWNER)
    return 'Отправьте ссылку на страницу владельца:'


@bot.on.private_message(state=AddCharData.OWNER)
async def owner_handler(message: Message):
    name = ctx.get('name')
    blank_id = ctx.get('blank_id')
    count = ctx.get('blank_count')
    owner = message.text
    sql.execute(f'INSERT INTO characters VALUES (?, ?, ?, ?)', (name, blank_id, count, owner))
    await message.answer('Персонаж успешно добавлен!')
    ctx.delete('name')
    ctx.delete('blank_id')
    ctx.delete('blank_count')
    await bot.state_dispenser.delete(message.peer_id)
    return 'Вы вернулись в общее меню.'
