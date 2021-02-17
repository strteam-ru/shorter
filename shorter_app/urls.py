from django.urls import path, re_path
from .views import IndexFormView, CheckShortLinkView, RedirectView, UrlNotFoundView
from .api_views import GetShortLinkViews, GetUserLinksViews, SaveLinkViews, CheckShortLinkViews

urlpatterns = [
    path('', IndexFormView.as_view()),
    path('404/', UrlNotFoundView.as_view()),
    path('<int:page>/', IndexFormView.as_view()),
    path('ajax/check_short_link', CheckShortLinkView.as_view()),
    path('api/v1/get_short_link', GetShortLinkViews.as_view()),
    path('api/v1/check_short_link', CheckShortLinkViews.as_view()),
    path('api/v1/get_user_links', GetUserLinksViews.as_view()),
    path('api/v1/save_link', SaveLinkViews.as_view()),
    re_path(r'\w{1,10}', RedirectView.as_view()),
]
