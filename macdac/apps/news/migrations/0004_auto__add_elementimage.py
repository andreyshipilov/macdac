# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ElementImage'
        db.create_table('news_elementimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('element', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['news.Element'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('news', ['ElementImage'])


    def backwards(self, orm):
        # Deleting model 'ElementImage'
        db.delete_table('news_elementimage')


    models = {
        'news.element': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Element'},
            'allow_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'full': ('django.db.models.fields.TextField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['news.Source']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'})
        },
        'news.elementimage': {
            'Meta': {'object_name': 'ElementImage'},
            'element': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['news.Element']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
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