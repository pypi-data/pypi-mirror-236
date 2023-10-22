from . import *
from . import urls
import logging

from .base import connectApi, headerGenerate

logger = logging.getLogger('libhoyolab.games')


class Genshin:
    @staticmethod
    def dailyNote():
        header = headerGenerate(client='2', salt_agro2='6x', agro=2)
        resp = session.get(urls.dailyNote_genshin_widget, headers=header)
        notes = resp.json()
        return notes


class StarRail:
    @staticmethod
    def dailyNote():
        header = headerGenerate(client='2', salt_agro2='6x', agro=2)
        resp = session.get(urls.dailyNote_hkrpg_widget, headers=header)
        print(resp.text)
        notes = resp.json()
        return notes