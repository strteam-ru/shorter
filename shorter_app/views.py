import json
import re

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from .logger import logger
from .classes import Link, ShortLink, Hits, User
from .forms import LinksForm
from .forms import ShortLinksForm


class IndexFormView(View):
    """
        index page
        get - generate index page
        post - add link record
    """

    def get(self, request, page=1):
        short_link = ShortLink.create()
        try:
            user_links = Link.get_user_links(request.session['user_id'], page)
            data = {"short_link": short_link,
                    'record_list': user_links,
                    'pages': range(1, user_links.paginator.num_pages + 1),
                    'server': request.get_host
                    }
        except KeyError:
            data = {"short_link": short_link,
                    'record_list': '',
                    'pages': '',
                    'server': request.get_host
                    }
            logger.info('unknown user')
        logger.info('index display with page {}'.format(page))
        return render(request, "index.html", context=data)

    def post(self, request):
        logger.info('link add start')
        links = LinksForm(request.POST)
        try:
            user = User.get_user(request.session.get('user_id'))
        except:
            data = {"result": False, 'errors': 'User not exist'}
            logger.error('User not exist - {}'.format(request.session.get('user_id')))
            return HttpResponse(json.dumps(data), status=200)
        request.session['user_id'] = user.id
        link = Link.save_form(links, user, request.get_host())
        if link.status:
            data = {"result": True}
            logger.info('link added')
            status = 201
        else:
            data = {"result": False, 'errors': link.errors}
            logger.warning('link add error - {}'.format(link.errors))
            status = 200
        Hits.run_hits()
        return HttpResponse(json.dumps(data), status=status)


class CheckShortLinkView(View):
    """AJAX short_link check for correctness and uniqueness """

    def post(self, request):
        links_form = ShortLinksForm(request.POST)
        if not links_form.is_valid():
            data = {"result": False, "value": links_form.errors.get('short_link')}
            logger.warning('short link error {}'.format(links_form.errors.get('short_link')))
        else:
            result, value = ShortLink.check_short_link(links_form.cleaned_data.get('short_link'))
            data = {"result": result, "value": value}
            logger.info('short link checked')
        return HttpResponse(json.dumps(data), status=200)


class RedirectView(View):
    """redirect to full link"""

    def get(self, request):
        short_link = re.sub("[^A-Za-z]", "", request.path)
        full_link = Link.get_full_link(short_link)
        logger.info('redirect from {} to {}'.format(short_link, full_link))
        return redirect(full_link)


class UrlNotFoundView(View):
    """Error 404"""

    def get(self, request):
        logger.warn('error request {}'.format(request.path))
        return render(request, "404.html")
