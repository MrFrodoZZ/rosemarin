from vkbottle.bot import Blueprint, Message
from vkbottle import API
import config as cfg


bot = Blueprint('Получение правил')
app = API(token=cfg.api_key)
bot.on.vbml_ignore_case = True


@bot.on.private_message(text=['/rules <part:int>', '/rules'])
async def get_rules(message: Message, part=None):

    if part is not None:

        data = await app.board.get_comments(
            cfg.g_id,
            cfg.rules_id,
            offset=1
        )

        if part == 0:
            await message.answer(data.items[0].text)
            await message.answer(data.items[1].text)
            await message.answer(data.items[2].text)
            await message.answer(data.items[3].text)
        elif part == 1:
            await message.answer(data.items[0].text)
        elif part == 2:
            await message.answer(data.items[1].text)
        elif part == 3:
            await message.answer(data.items[2].text)
        elif part == 4:
            await message.answer(data.items[3].text)
        else:
            await message.answer(cfg.rules_noarg)
    else:
        await message.answer(cfg.rules_noarg)
