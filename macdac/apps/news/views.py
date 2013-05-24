from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import RedirectView
from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
                                        MonthArchiveView, DayArchiveView,
                                        DateDetailView)
from django.shortcuts import get_object_or_404

from .models import Source, Element


class HomeView(ArchiveIndexView):
    "Home page view."

    model = Element
    date_field = "date"
    allow_future = True
    template_name = "news/home.html"
    paginate_by = settings.PAGINATION_DEFAULT_PAGINATION

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({"is_home": True})

        return context


class SourceView(ArchiveIndexView):
    "One single source page view."

    model = Element
    date_field = "date"
    allow_future = True
    template_name = "news/source.html"

    def get_queryset(self, **kwargs):
        qs = super(SourceView, self).get_queryset(**kwargs)
        qs = qs.filter(source__slug=self.kwargs.get('source_slug'))

        return qs

    def get_context_data(self, **kwargs):
        context = super(SourceView, self).get_context_data(**kwargs)
        current_source = get_object_or_404(Source,
                                           slug=self.kwargs.get('source_slug'))
        context.update({
            'current_source': current_source,
            'is_source_page': True,
        })

        return context


class YearView(YearArchiveView):
    "Source's year page view."

    model = Element
    date_field = "date"
    allow_future = True
    template_name = "news/year.html"
    make_object_list = True

    def get_queryset(self, **kwargs):
        qs = super(YearView, self).get_queryset(**kwargs)
        qs = qs.filter(source__slug=self.kwargs.get('source_slug'))

        return qs

    def get_context_data(self, **kwargs):
        context = super(YearView, self).get_context_data(**kwargs)
        current_source = get_object_or_404(Source,
                                           slug=self.kwargs.get('source_slug'))
        context.update({
            'current_source': current_source,
        })

        return context


class MonthView(MonthArchiveView):
    "Source's month page view."

    model = Element
    date_field = "date"
    month_format = "%B"
    allow_future = True
    template_name = "news/month.html"

    def get_queryset(self, **kwargs):
        qs = super(MonthView, self).get_queryset(**kwargs)
        qs = qs.filter(source__slug=self.kwargs.get('source_slug'))

        return qs

    def get_context_data(self, **kwargs):
        context = super(MonthView, self).get_context_data(**kwargs)
        current_source = get_object_or_404(Source,
                                           slug=self.kwargs.get('source_slug'))
        context.update({
            'current_source': current_source,
        })

        return context


class DayView(DayArchiveView):
    "Source's day page view."

    model = Element
    date_field = "date"
    month_format = "%B"
    allow_future = True
    template_name = "news/day.html"

    def get_queryset(self, **kwargs):
        qs = super(DayView, self).get_queryset(**kwargs)
        qs = qs.filter(source__slug=self.kwargs.get('source_slug'))

        return qs

    def get_context_data(self, **kwargs):
        context = super(DayView, self).get_context_data(**kwargs)
        current_source = get_object_or_404(Source,
                                           slug=self.kwargs.get('source_slug'))
        context.update({
            'current_source': current_source,
            'month': self.get_month(),
        })

        return context


class ElementView(DateDetailView):
    "Single news element."

    model = Element
    context_object_name = "object"
    date_field = "date"
    month_format = "%B"
    allow_future = True
    template_name = "news/element.html"

    def get_queryset(self, **kwargs):
        qs = super(ElementView, self).get_queryset(**kwargs)
        qs = qs.filter(source__slug=self.kwargs.get('source_slug'))

        return qs

    def get_context_data(self, **kwargs):
        context = super(ElementView, self).get_context_data(**kwargs)
        current_source = get_object_or_404(Source,
                                           slug=self.kwargs.get('source_slug'))
        context.update({
            'current_source': current_source,
            'month': self.get_month(),
        })

        return context


class RedirectFromShort(RedirectView):
    "Redirects from a given 'pk' in url to a full news element."

    permanent = True
    query_string = True

    def get_redirect_url(self, pk):
        obj = get_object_or_404(Element.get_available(), pk=pk)

        return reverse_lazy('news_element', args=(), kwargs={
            'source_slug': obj.source.slug,
            'year': obj.date.year,
            'month': obj.date.strftime("%B").lower(),
            'day': obj.date.day,
            'slug':  obj.slug,
        })


def get_news(request):
    "Get a list of news after certain date for endless scroll."

    if request.method != 'POST':
        raise Http404

    max_pk = request.POST.get('pk')
    max_date = get_object_or_404(Element, pk=max_pk).date
    qs = Element.get_available().filter(date__lte=max_date) \
        .exclude(pk=max_pk)[:settings.PAGINATION_DEFAULT_PAGINATION]

    return render(request, 'get_news.html', {
        'object_list': qs,
    })
