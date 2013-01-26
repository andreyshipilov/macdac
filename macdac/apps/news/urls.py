from django.conf.urls.defaults import patterns, url
from django.views.decorators.cache import cache_page
from django.views.generic.dates import ArchiveIndexView

from .feeds import NewsFeed, RSSRedirectView
from .models import Source, Element
from .views import (SourceView, YearView, MonthView, DayView, ElementView,
                    HomeView, RedirectFromShort)


HOUR = 60 * 60

urlpatterns = patterns('news.views',
    url(r'^(?P<source_slug>[a-z0-9]+)/$', cache_page(HOUR)(SourceView.as_view()),
        name='news_source'),
    url(r'^(?P<source_slug>[a-z0-9]+)/(?P<year>\d{4})/$', cache_page(HOUR)(YearView.as_view()),
        name='news_year'),
    url(r'^(?P<source_slug>[a-z0-9]+)/(?P<year>\d{4})/(?P<month>[a-z]{3,10})/$',
        cache_page(HOUR)(MonthView.as_view()), name='news_month'),
    url(r'^(?P<source_slug>[a-z0-9]+)/(?P<year>\d{4})/(?P<month>[a-z]{3,10})/(?P<day>\d{1,2})/$',
        cache_page(HOUR)(DayView.as_view()), name='news_day'),
    url(r'^(?P<source_slug>[a-z0-9]+)/(?P<year>\d{4})/(?P<month>[a-z]{3,10})/(?P<day>\d{1,2})/(?P<slug>[-\w_]+)/$',
        cache_page(HOUR)(ElementView.as_view()), name='news_element'),

    url(r'^rss-redirect$', RSSRedirectView.as_view(), name="rss_redirect"),
    url(r'^rss$', NewsFeed()),
    url(r'^(?P<pk>\d+)$', RedirectFromShort.as_view(),
        name="redirect_from_short"),

    url(r'^get-news/$', 'get_news', name="get_news"),
    url(r'^$', HomeView.as_view(), name="news_index"),
)
