from os.path import splitext
from os import urandom
import re

from django.db import models
from django.contrib.sites.models import Site

from cached_counter.counters import Counter
from sorl.thumbnail import ImageField, get_thumbnail


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
        return ('news_source', (), {'source_slug': self.slug})

    def get_element_count(self):
        return Element.get_available(source_slug=self.slug).count()


class Element(models.Model):
    date = models.DateTimeField(db_index=True)
    date_start_publication = models.DateTimeField(blank=True, null=True,
                                                  db_index=True,)
    title = models.CharField(max_length=200, db_index=True,)
    slug = models.SlugField(max_length=200, unique_for_date="date",)
    full = models.TextField(db_index=True,)
    full_prepared = models.TextField(blank=True,
                                     help_text="Will be overwritten on save.")
    link = models.URLField(max_length=500, blank=True,)
    source = models.ForeignKey(Source,)
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

    def get_full(self):
        return self.full_prepared if self.full_prepared else self.full

    def process_images_tags(self):
        "Process full text, parse image tags, replace with html."

        text = self.full
        match = re.findall("({{\s*(\w+)\s*}})", text)

        for i in match:
            text_tag, tag = i

            try:
                img = self.images.only("image", "width").get(tag=tag)
                thumb = get_thumbnail(img.image, "%sx1000" % img.width,
                                      quality=80, upscale=False,)
                template = '<img src="%s" width="%s" height="%s" alt="%s" />' % \
                           (thumb.url, thumb.width, thumb.height, self.title)
                text = text.replace(text_tag, template)
            except Exception, e:
                print e

        return text

    def save(self, *args, **kwargs):
        "Prepare the full text before every save."

        self.full_prepared = self.process_images_tags()
        models.Model.save(self, *args, **kwargs)


class ElementImage(models.Model):
    element = models.ForeignKey(Element, related_name="images",)
    tag = models.CharField(max_length=20, blank=True,)
    image = ImageField(blank=True,
                       upload_to=lambda i, f: "macdac-news/%s%s" % \
                       (urandom(16).encode("hex"), splitext(f)[1].lower()),)
    width = models.CharField(choices=(("300", "300 px"), ("600", "600 px")),
                             default="300", max_length=3,)

    class Meta:
        verbose_name = "image"

    def __unicode__(self):
        return self.tag if self.tag else "image"
