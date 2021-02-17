import random
import string
import re

from shorter import settings
from ..logger import logger
from ..models import Links


class ShortLink:
    @staticmethod
    def create() -> str:
        short_link = ''.join(random.choice(string.ascii_lowercase) for i in range(settings.SHORT_LINK_LENGTH))
        logger.info('created short link - {}'.format(short_link))
        return short_link

    @staticmethod
    def check_unique(short_link: str) -> bool:
        return True if Links.objects.filter(short_link=short_link).count() == 0 else False

    @staticmethod
    def check_short_link(short_link: str) -> bool:
        short_link = ShortLink.clear_bed_symbols(short_link)
        if len(short_link) < 2:
            logger.warning('short link not valid')
            return False, 'Значение короткой ссылки не верно'
        elif not ShortLink.check_unique(short_link):
            logger.warning('short link is not unique')
            return False, 'Значение короткой ссылки не уникально'
        else:
            logger.info('short link is valid')
            return True, short_link

    @staticmethod
    def clear_bed_symbols(link: str) -> str:
        reg = re.sub('[^a-z]{1,10}', '', link)
        return reg
