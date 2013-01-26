# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Source', fields ['is_alive']
        db.create_index('news_source', ['is_alive'])

        # Deleting field 'element.is_published'
        db.delete_column('news_element', 'is_published')

        # Adding field 'Element.slug'
        db.add_column('news_element', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default=1, max_length=200),
                      keep_default=False)

        # Adding index on 'Element', fields ['full']
        db.create_index('news_element', ['full'])

        # Adding index on 'Element', fields ['title']
        db.create_index('news_element', ['title'])

        # Adding index on 'Element', fields ['date']
        db.create_index('news_element', ['date'])


    def backwards(self, orm):
        # Removing index on 'Element', fields ['date']
        db.delete_index('news_element', ['date'])

        # Removing index on 'Element', fields ['title']
        db.delete_index('news_element', ['title'])

        # Removing index on 'Element', fields ['full']
        db.delete_index('news_element', ['full'])

        # Removing index on 'Source', fields ['is_alive']
        db.delete_index('news_source', ['is_alive'])

        # Adding field 'element.is_published'
        db.add_column('news_element', 'is_published',
                      self.gf('django.db.models.fields.BooleanField')(default=True, blank=True),
                      keep_default=False)

        # Deleting field 'Element.slug'
        db.delete_column('news_element', 'slug')


    models = {
        'news.element': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Element'},
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'full': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['news.Source']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        },
        'news.source': {
            'Meta': {'ordering': "['-is_alive', 'title']", 'object_name': 'Source'},
            'homepage': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_alive': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'rss_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['news']