from django.contrib.sites.models import Site
from django.template import Library
from django.db.models import Count

from news.models import Source



register = Library()

def sources_list(context):
    "List of sources on every news page."""

    return {
        'current_source': context.get('current_source', None),
        'is_source_page': context.get('is_source_page', False),
        'alive': Source.objects.filter(is_alive=True) \
                       .annotate(count=Count('element')).filter(count__gte=1).order_by('-count'),
        'dead': Source.objects.filter(is_alive=False) \
                      .annotate(count=Count('element')).filter(count__gte=1).order_by('-count'),
    }
register.inclusion_tag('sources_list.html', takes_context=True)(sources_list)
