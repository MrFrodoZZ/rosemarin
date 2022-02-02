from vkbottle.bot import Blueprint, Message
from vkbottle import API, CtxStorage
import config as cfg
import sqlite3


bot = Blueprint('Получение анкеты')
app = API(token=cfg.api_key)
ctx = CtxStorage()
db = sqlite3.connect('data.db')
sql = db.cursor()
bot.on.vbml_ignore_case = True


@bot.on.chat_message(text='/char')
async def pers_info(message: Message):
    if message.from_id not in cfg.admins:
        await message.answer(cfg.chat_not_admin)
    else:
        await message.answer(cfg.persinfo_noarg)


# @bot.on.chat_message(rules.CommandRule('char', ['/', '!'], 1))
# async def pers_info_onlyname(message: Message, args: Tuple[str]):
#     if message.from_id in cfg.admins:
#         if args[0].isalpha():
#             search = args[0].capitalize()
#             result = sql.execute(f"SELECT * FROM characters WHERE name LIKE '%{search}%'").fetchone()
#             if result:
#                 owner = sql.execute(f'SELECT name, link FROM owners WHERE id = "{result[2]}"').fetchone()
#                 comment_id = int(result[3].split('=')[1])
#
#                 blank = await app.board.get_comments(
#                     cfg.g_id,
#                     cfg.blanks_id,
#                     start_comment_id=comment_id,
#                     count=result[4]
#                 )
#
#                 arts = ''
#                 items = blank.items
#                 for i in range(len(items)):
#                     if items[i].attachments is not None:
#                         media = []
#                         audios = []
#                         for j in range(len(items[i].attachments)):
#                             if items[i].attachments[j].photo:
#                                 curr = items[i].attachments[j].photo
#                                 a_owner = curr.owner_id
#                                 if a_owner == -cfg.g_id:
#                                     media.append(f'photo{str(-cfg.g_id)}_{items[i].attachments[j].photo.id}')
#                                 else:
#                                     media.append(f'photo{a_owner}_{curr.id}_{curr.access_key}')
#                             elif items[i].attachments[j].audio:
#                                 curr = items[i].attachments[j].audio
#                                 audios.append(f'audio{curr.owner_id}_{curr.id}_{curr.access_key}')
#                         arts = ','.join(s for s in media) + ','
#                         arts += ','.join(m for m in audios)
#
#                 fin = ''
#                 fin_data = [result[1], owner[0], owner[1]]
#
#                 for i in range(len(cfg.char_info)):
#                     fin += cfg.char_info[i] + fin_data[i]
#
#                 await message.answer(fin, arts)
#
#             else:
#                 await message.answer(cfg.char_not_found)
#
#         else:
#             await message.answer(cfg.persinfo_noarg)
#     else:
#         await message.answer(cfg.chat_not_admin)
#
#
# @bot.on.chat_message(rules.CommandRule('char', ['/', '!'], 2))
# async def pers_info_fullname(message: Message, args: Tuple[str]):
#     if message.from_id in cfg.admins:
#         if args[0].isalpha() and args[1].isalpha():
#             search = args[0].capitalize() + ' ' + args[1].capitalize()
#             result = sql.execute(f"SELECT * FROM characters WHERE name LIKE '%{search}%'").fetchone()
#             if result:
#                 owner = sql.execute(f'SELECT name, link FROM owners WHERE id = "{result[2]}"').fetchone()
#                 comment_id = int(result[3].split('=')[1])
#
#                 blank = await app.board.get_comments(
#                     cfg.g_id,
#                     cfg.blanks_id,
#                     start_comment_id=comment_id,
#                     count=result[4]
#                 )
#
#                 arts = ''
#                 items = blank.items
#                 for i in range(len(items)):
#                     if items[i].attachments is not None:
#                         media = []
#                         audios = []
#                         for j in range(len(items[i].attachments)):
#                             if items[i].attachments[j].photo:
#                                 curr = items[i].attachments[j].photo
#                                 a_owner = curr.owner_id
#                                 if a_owner == -cfg.g_id:
#                                     media.append(f'photo{str(-cfg.g_id)}_{items[i].attachments[j].photo.id}')
#                                 else:
#                                     media.append(f'photo{a_owner}_{curr.id}_{curr.access_key}')
#                             elif items[i].attachments[j].audio:
#                                 curr = items[i].attachments[j].audio
#                                 audios.append(f'audio{curr.owner_id}_{curr.id}_{curr.access_key}')
#                         arts = ','.join(s for s in media) + ','
#                         arts += ','.join(m for m in audios)
#
#                 fin = ''
#                 fin_data = [result[1], owner[0], owner[1]]
#                 for i in range(len(cfg.char_info)):
#                     fin += cfg.char_info[i] + fin_data[i]
#                 await message.answer(fin, arts)
#
#             else:
#                 await message.answer(cfg.char_not_found)
#
#         else:
#             await message.answer(cfg.persinfo_noarg)
#
#     else:
#         await message.answer(cfg.chat_not_admin)