from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from util.decorators import allow_methods

from model import *

@allow_methods('GET')
def main_page(request, page=1):
    item_list = Item.objects.order_by('-item_date')
    paginator = Paginator(item_list, 9)  # shows 9 items per page
    
    try:
        page = int(page)
    except ValueError:
        page = 1
        
    # If page request(9999) is out of range, deliver last page of the results
    try:
        items = paginator.page(page)
    except (EmptyPage, InvalidPage):
        items = paginator.page(paginator.num_pages)
    
    return direct_to_template(request, "main.tpl", {"items" : items})    

