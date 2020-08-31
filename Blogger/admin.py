# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
	list_display=["title", "created_date", "published_date"]
	list_display_links=["created_date"]
	list_filter=["created_date", "published_date"]
	list_editable=["title", "published_date"]
	search_fields=["title", "text"]
	class Meta:
		model=Post

admin.site.register(Post, PostAdmin)

# Register your models here.
