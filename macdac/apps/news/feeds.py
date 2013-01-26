from django.contrib.syndication.views import Feed
from django.views.generic.base import RedirectView

from .models import Element



class NewsFeed(Feed):
    link = '/'

    def items(self):
        return Element.get_available()[:20]

    def item_title(self, item):
        return item.title


class RSSRedirectView(RedirectView):
    "Redirects to a real FeedBurner url."""

    permanent = True

    def get_redirect_url(self):
        # Yeah yeah, hardcoded...
        url = "http://feeds.feedburner.com/macdac"

        return url
