from F.Feed.models import *
from django.contrib import admin
from lifestream.models import LifeStream

admin.site.register(Feed)
admin.site.register(User)
admin.site.register(LifeStream)
admin.site.register(Item)
admin.site.register(Tag)