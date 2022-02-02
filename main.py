# -*- coding: utf-8 -*-
from vkbottle.bot import Bot
from vkbottle import load_blueprints_from_package
import config as cfg


bot = Bot(token=cfg.token)


for bp in load_blueprints_from_package('blueprints\\private'):
    bp.load(bot)

for bp in load_blueprints_from_package('blueprints'):
    bp.load(bot)


bot.run_forever()
