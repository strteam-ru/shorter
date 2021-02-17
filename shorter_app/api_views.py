import json

from rest_framework.response import Response
from rest_framework.views import APIView

from .logger import logger
from .serializers import LinksSerializer, HostSerializer, UserSerializer, UserLinksSerializer, SortLinkSerializer
from .classes import Link, ShortLink, Hits, User


class GetShortLinkViews(APIView):
    """generate short link"""

    def post(self, request):
        short_link = ShortLink.create()
        logger.info('short link created')
        return Response(short_link)


class CheckShortLinkViews(APIView):
    """
    check short link
    request:
    short_link
    response:
    result, short_link, errors
    """

    def post(self, request):
        short_link = SortLinkSerializer(data=request.data)
        if not short_link.is_valid():
            result = False
            errors = short_link.errors
            status = 400
        else:
            result, value = ShortLink.check_short_link(short_link.data.get('short_link'))
            if not result:
                errors = value
                status = 400
            else:
                result = False
                short_link = value
                status = 200
        return Response({'result': result, 'short_link': short_link, 'errors': errors}, status=status)


class GetUserLinksViews(APIView):
    """
    get usr links from db
    request:
    user_id, page
    response:
    page - current page
    pages - max user pages
    records - link records list
    errors - check errors
    """

    def post(self, request):
        user = UserSerializer(data=request.data)
        if not user.is_valid():
            logger.warning('user not valid {}'.format(user.errors))
            return Response({'result': False, 'errors': user.errors}, status=400)
        else:
            user_links = Link.get_user_links(user.data.get('user_id'), user.data.get('page'))
            links = []
            for link in user_links:
                links.append(UserLinksSerializer(link).data)
            data = {'page': user_links.number, 'pages': user_links.paginator.num_pages, 'records': links}
            Hits.run_hits()
            return Response({'result': True, 'value': data}, status=200)


class SaveLinkViews(APIView):
    """
    save link to db
    request:
    user_id, short_link, full_link, host
    response:
    result, errors
    """

    def post(self, request):
        links = LinksSerializer(data=request.data)
        if not links.is_valid():
            logger.warning('link data error {}'.format(links.errors))
            result = False
            errors = links.errors
            status = 400
        else:
            host = HostSerializer(data=request.data)
            if not host.is_valid():
                logger.warning('host data error {}'.format(host.errors))
                result = False
                errors = host.errors
                status = 400
            else:
                try:
                    user = User.get_user(links.data.get('user_id'))
                    link = Link.save_api(links, user, host)
                    result = link.status
                    errors = link.errors
                    status = link.status_code
                    logger.info('link saved {}-{}'.format(link.short_link, link.full_link))
                except:
                    logger.warning('user not found {}'.format(links.data.get('user_id')))
                    result = False
                    errors = 'User not found'
                    status = 400
        return Response({'result': result, 'errors': errors}, status=status)
