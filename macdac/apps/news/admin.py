from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Source, Element, ElementImage



class SourceAdmin(admin.ModelAdmin):
    list_filter = ['is_alive', 'site',]
    fieldsets = [
	('Site dependency', {'fields': ('site',)}),
	('Is a working site', {'fields': ('is_alive',)}),
	('Source info', {'fields': ('title', 'slug', 'homepage', 'rss_link',)}),
    ]
admin.site.register(Source, SourceAdmin)


class ElementImageAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ("element", "tag")
admin.site.register(ElementImage, ElementImageAdmin)

class ElementImageInline(admin.TabularInline):
    model = ElementImage


class ElementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'source',)
    list_filter = ['source',]
    date_hierarchy = 'date'
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ElementImageInline,)

    fieldsets = [
	(None, {'fields': ('title', 'slug',)}),
	('News texts', {'fields': ('full', 'allow_comments',)}),
	('Source data', {'fields': ('link', 'source',)}),
	('Date of source publishing', {'fields': ('date',), 'classes': 'collapse'}),
    ]
admin.site.register(Element, ElementAdmin)