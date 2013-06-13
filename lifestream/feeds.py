from util import stripper
from util import feedparser
from django.utils.http import urlquote
from django.db.models import Q

from models import *

import datetime
import dateutil.parser

def update_defs():
    feeds = Feed.objects.filter(feed_deleted=False)
    for feed in feeds:
        try:
            feed_items = feedparser.parse(feed.feed_url)
            for entry in feed_items['entries']:
                date_published = entry.get('published', entry.get('updated'))
                if not date_published:
                    date_published = str(datetime.datetime.utcnow())
                
                protocol_index = entry['link'][0:7].find("://")
                if protocol_index != -1:
                    permalink = entry['link'][:protocol_index+3] + urlquote(entry['link'][protocol_index+3:])
                else:
                    permalink = urlquote(entry['link'])
                
                date_published = dateutil.parser.parse(date_published)
                
                date_published = (date_published - date_published.utcoffset()).replace(tzinfo=None)
                
                items_count = Item.objects.filter(
                                                  Q(item_date = date_published) |
                                                  Q(item_permalink = permalink)).filter(
                                                                                        item_feed = feed).count()
                
                if items_count == 0:
                    feed_content = entry.get('content')
                    if feed_content is not None:
                        feed_content = feed_content[0]['value']
                        content = stripper.strip_tags(feed_content)
                        clean_content = stripper.strip_tags(feed_content, ())
                    else:
                        content = None
                        clean_content = None
                    
                    i = Item(item_feed = feed,
                             item_date = date_published,
                             item_title = entry.get('title'),
                             item_content = content,
                             item_clean_content = clean_content,
                             item_author = entry.get('author'),
                             item_permalink = permalink
                             )
                    i.save()
                    
                    tags = ()
                    if 'tags' in entry:
                        for tag in entry['tags']:
                            slug  = urlquote(tag.get('term').lower())
                            try:
                                tagobj = Tag.objects.get(tag_slug=slug)
                            except:
                                tagobj = Tag(tag_name = tag['term'],
                                             tag_slug = slug,
                                             tag_count = 1)
                                tagobj.save()
                            i.item_tags(tagobj);
                        i.save()
                                                                                            
                                                                                    
        except Exception, e:
            print e                                          
                    