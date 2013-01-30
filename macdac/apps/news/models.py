from os.path import splitext
from os import urandom

from django.db import models
from django.contrib.sites.models import Site

from cached_counter.counters import Counter
from sorl.thumbnail import ImageField



class Source(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    homepage = models.CharField(max_length=50)
    rss_link = models.URLField()
    is_alive = models.BooleanField(default=False, db_index=True)
    site = models.ForeignKey(Site)
    count = Counter("get_element_count")

    class Meta:
	ordering = ['-is_alive', 'title']

    def __unicode__(self):
	return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('news_source', (), {'source_slug': self.slug,})

    def get_element_count(self):
        return Element.get_available(source_slug=self.slug).count()


class Element(models.Model):
    date = models.DateTimeField(db_index=True)
    date_start_publication = models.DateTimeField(blank=True, null=True, db_index=True,)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique_for_date="date")
    full = models.TextField(db_index=True)
    link = models.URLField(max_length=500, blank=True,)
    source = models.ForeignKey(Source)
    allow_comments = models.BooleanField(default=True,)

    class Meta:
	ordering = ['-date']

    def __unicode__(self):
	return self.title

    @staticmethod
    def get_available(source_slug=None):
        qs = Element.objects.all()

        if source_slug:
            qs = qs.filter(source__slug=source_slug)

        return qs

    @models.permalink
    def get_absolute_url(self):
        return ('news_element', (), {
            "year": self.date.year,
            "month": self.date.strftime("%B").lower(),
            "day": self.date.day,
            "slug": self.slug,
            "source_slug": self.source.slug,
        })

    def get_short_url(self):
        return "http://%s/%s" % (self.source.site.domain, self.pk)

    def get_previous(self):
	return self.get_previous_by_date(source=self.source)

    def get_next(self):
	return self.get_next_by_date(source=self.source)


class ElementImage(models.Model):
    element = models.ForeignKey(Element)
    tag = models.CharField(max_length=20, blank=True,)
    image = ImageField(blank=True, upload_to=lambda i, f: "macdac-news/%s%s" % \
                          (urandom(16).encode("hex"), splitext(f)[1].lower()),)
