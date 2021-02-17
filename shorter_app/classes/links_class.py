from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

from shorter import settings
from ..logger import logger
from ..models import Links
from .short_links_calss import ShortLink


class Link:
    """short-full link"""

    def __init__(self, short_link='', full_link='', user=0, host=''):
        self.short_link = short_link
        self.full_link = full_link
        self.host = host
        self.user = user
        self.status = True
        self.status_code = 201
        self.errors = ''

    def save_link(self):
        if self.check_links():
            link = Links(user_id=self.user, short_link=self.short_link, full_link=self.full_link)
            link.save()
            logger.info('new link created {} - {}'.format(self.short_link, self.full_link))
            return True
        else:
            return False

    def check_links(self):
        result, message = ShortLink.check_short_link(self.short_link)
        if not result:
            self.errors = message
            logger.warning('short link is not valid - {}'.format(self.short_link))
            return False
        elif not self.check_full_link():
            return False
        elif not self.check_link_recursion():
            self.errors = 'Циклическая ссылка'
            logger.warning('recursion link - {} - {}'.format(self.short_link, self.full_link))
            return False
        else:
            self.short_link = message
            logger.info('short link is valid - {}'.format(self.short_link))
            return True

    def check_full_link(self):
        regular = '^https{,1}://.*'
        if re.match(regular, self.full_link) is not None:
            logger.info('full link is valid - {}'.format(self.full_link))
            return True
        else:
            self.errors = 'Full link не является ссылкой http/https протокола'
            logger.warning('full link is not link - {}'.format(self.full_link))
            return False

    def check_link_recursion(self):
        regular = '^https{,1}://' + self.host + '.*'
        if re.match(regular, self.full_link) is not None:
            print(re.match(regular, self.full_link))
            self.errors = 'Рекурсивня ссылка {}'.format(self.full_link)
            logger.warning('full link recursion - {}'.format(self.full_link))
            return False
        else:
            return True

    @staticmethod
    def save_form(links, user, host):
        link = Link()
        if not links.is_valid():
            link.status = False
            link.errors = links.errors
            logger.error('new link creat error {}'.format(links.errors))
        else:
            link.short_link = links.cleaned_data.get('short_link')
            link.full_link = links.cleaned_data.get('full_link')
            link.host = host
            link.user = user
            link.status = True if link.save_link() else False
        return link

    @staticmethod
    def save_api(links, user, host):
        link = Link()
        if not host.is_valid():
            link.status = False
            link.errors = host.errors
            logger.error('new link creat error {}'.format(host.errors))
            link.status_code = 400
            return link
        link.short_link = links.data.get('short_link')
        link.full_link = links.data.get('full_link')
        link.user = user
        link.host = host.data.get('host')
        if not link.save_link():
            link.status = False
            link.status_code = 400
        else:
            link.status = True
            link.status_code = 201
        return link

    @staticmethod
    def get_user_links(user: int, page: int = 1):
        """return user's link with pagination """
        user_links = Links.objects.filter(user_id=user).order_by('-created')
        paginator = Paginator(user_links, settings.STRING_ON_PAGE)
        try:
            links = paginator.page(page)
        except PageNotAnInteger:
            links = paginator.page(1)
        except EmptyPage:
            links = paginator.page(paginator.num_pages)
        return links

    @staticmethod
    def get_full_link(short_link: str) -> str:
        try:
            cache_link = Link.get_cache(short_link)
            if cache_link:
                logger.info('link found in cache')
                return cache_link
            else:
                link = Links.objects.get(short_link=short_link)
                logger.info('link found in DB')
                Link.set_cache(short_link, link.full_link)
                return link.full_link
        except:
            logger.warning('link not found')
            link = '/404/'
            return link

    @staticmethod
    def set_cache(short_link: str, full_link: str, redis=settings.redis, ttl=settings.CACHE_TTL):
        redis.setex(short_link, ttl, full_link.encode('utf-8'))
        logger.info('link added to cache')

    @staticmethod
    def get_cache(short_link: str, redis=settings.redis) -> str:
        try:
            return redis.get(short_link).decode('utf-8')
        except AttributeError:
            return ''
