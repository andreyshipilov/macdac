
from south.db import db
from django.db import models
from news.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Source'
        db.create_table('news_source', (
            ('id', orm['news.Source:id']),
            ('title', orm['news.Source:title']),
            ('slug', orm['news.Source:slug']),
            ('homepage', orm['news.Source:homepage']),
            ('rss_link', orm['news.Source:rss_link']),
            ('is_alive', orm['news.Source:is_alive']),
            ('site', orm['news.Source:site']),
        ))
        db.send_create_signal('news', ['Source'])
        
        # Adding model 'Element'
        db.create_table('news_element', (
            ('id', orm['news.Element:id']),
            ('date', orm['news.Element:date']),
            ('title', orm['news.Element:title']),
            ('full', orm['news.Element:full']),
            ('link', orm['news.Element:link']),
            ('source', orm['news.Element:source']),
        ))
        db.send_create_signal('news', ['Element'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Source'
        db.delete_table('news_source')
        
        # Deleting model 'Element'
        db.delete_table('news_element')
        
    
    
    models = {
        'news.element': {
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'full': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['news.Source']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'news.source': {
            'homepage': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_alive': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'rss_link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'sites.site': {
            'Meta': {'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    
    complete_apps = ['news']
