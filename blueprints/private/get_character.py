from vkbottle.bot import Blueprint, Message
from vkbottle import API, CtxStorage
import config as cfg
import sqlite3


bot = Blueprint('Получение анкеты и манипуляции с ней')
app = API(token=cfg.api_key)
ctx = CtxStorage()
db = sqlite3.connect(cfg.database)
sql = db.cursor()


@bot.on.private_message(text=['/char <name> <last>', '/char <name>', '/char'])
async def pers_info(message: Message, name=None, last=None):

    if name is not None and last is not None:
        search = name.capitalize() + ' ' + last.capitalize()
    elif name is not None:
        search = name.capitalize()
    else:
        return cfg.persinfo_noarg

    result = sql.execute(f"SELECT * FROM characters WHERE name LIKE '%{search}%'").fetchone()
    if result:
        owner = sql.execute(f'SELECT name, link FROM owners WHERE id = "{result[2]}"').fetchone()
        comment_id = int(result[3].split('=')[1])
        blank = await app.board.get_comments(
            cfg.g_id,
            cfg.blanks_id,
            start_comment_id=comment_id,
            count=result[4]
        )

        arts = ''
        items = blank.items
        for i in range(len(items)):
            if items[i].attachments is not None:
                media = []
                audios = []
                for j in range(len(items[i].attachments)):
                    if items[i].attachments[j].photo:
                        curr = items[i].attachments[j].photo
                        a_owner = curr.owner_id
                        if a_owner == -cfg.g_id:
                            media.append(f'photo{str(-cfg.g_id)}_{items[i].attachments[j].photo.id}')
                        else:
                            media.append(f'photo{a_owner}_{curr.id}_{curr.access_key}')
                    elif items[i].attachments[j].audio:
                        curr = items[i].attachments[j].audio
                        audios.append(f'audio{curr.owner_id}_{curr.id}_{curr.access_key}')
                arts = ','.join(s for s in media) + ','
                arts += ','.join(m for m in audios)

        if len(blank.items) > 1:
            blank2 = ''
            for i in range(len(blank.items)):
                blank2 += '\n' + blank.items[i].text
            blank = blank2
        else:
            blank = blank.items[0].text

        fin = ''
        fin_data = [result[1], owner[0], owner[1], blank]

        for i in range(len(cfg.char_info)):
            if i == 3:
                fin += cfg.char_info[i] + ' ' + fin_data[i]
            else:
                fin += cfg.char_info[i] + fin_data[i]
        fin += '\n\nЧтобы получить анкету персонажа введите: /anketa'
        ctx.set('blank', blank)

        if message.from_id in cfg.admins:
            fin += '\nЧтобы удалить персонажа введите: /delchar'
            ctx.set('delete', result[1])
            ctx.set('delete2', items)

        await message.answer(fin, arts)

    else:
        await message.answer(cfg.char_not_found)


@bot.on.private_message(text='/anketa')
async def send_blank(message: Message):
    if ctx.get('blank'):
        await message.answer(ctx.get('blank'))
        ctx.delete('blank')
    else:
        await message.answer(cfg.char_no_blank)


@bot.on.private_message(text='/delchar')
async def delete_char(message: Message):
    if ctx.get('delete'):
        sql.execute(f'DELETE FROM characters WHERE name = "{ctx.get("delete")}"')
        items = ctx.get('delete2')
        for i in range(len(items)):
            await bot.api.board.delete_comment(
                cfg.g_id,
                cfg.blanks_id,
                items[i].id
            )
        ctx.delete('delete')
        ctx.delete('delete2')
        db.commit()
        await message.answer('Удалено.')
    else:
        await message.answer('Не выбрана анкета.')
