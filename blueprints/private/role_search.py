from vkbottle.bot import Blueprint, Message
from vkbottle import API
import config as cfg


bot = Blueprint('Поиск сорола')
app = API(token=cfg.api_key)