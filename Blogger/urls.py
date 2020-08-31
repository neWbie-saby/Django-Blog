from django.conf.urls import include, url
from django.contrib import admin

import Blogger
from Blogger import views as hviews

from . import views

urlpatterns = [
    url(r'^$', hviews.post_list, name='list'),
    url(r'^create/$', hviews.post_create),
    #url(r'^detail/(?P<id>\d+)/$', hviews.post_detail),
    url(r'^(?P<slug>[\w-]+)/$', hviews.post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', hviews.post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', hviews.post_delete),
]
