# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib.parse import quote_plus
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q

from .models import Post
from .forms import PostForm

# Create your views here.

#def post_home(request):
#	return HttpResponse("<h1>Hello</h1>")

def post_create(request): #create
	if not request.user.is_staff:  #or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		#print(form.cleaned_data.get('title'))
		instance.save()
		messages.success(request, "Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	#else:
	#elif request.POST:
	#	messages.error(request, "Not successfully Created")

	#if request.method == 'POST':
	#	print(request.POST.get('text'))
	#	print(request.POST.get('title'))
	context = {"form" : form}
	return render(request, "post_form.html", context)
	#return HttpResponse("<h1>Create</h1>")

def post_detail(request, slug=None): #retrieve
	#instance = Post.objects.get(id=4)
	#instance = get_object_or_404(Post, title="Inside Django IPython shell")
	instance = get_object_or_404(Post, slug=slug)
	if instance.published_date > timezone.now() or instance.draft:
		if (not request.user.is_staff) or (not request.user.is_superuser):
			raise Http404
	share_str = quote_plus(instance.text)
	context = { "title" : instance.title,
		     "instance" : instance,
			"share_string" : share_str }	
	return render(request, "post_detail.html", context)	
	#return HttpResponse("<h1>Detail</h1>")

def post_list(request): #list items
	today = timezone.now()
	queryset_list = Post.objects.active()  #filter(draft=False).filter(published_date__lte=timezone.now())  #all().order_by("-published_date")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
					Q(title__icontains=query) |
					Q(text__icontains=query) |
					Q(user__first_name__icontains=query) |
					Q(user__last_name__icontains=query)
						    ).distinct()
	paginator = Paginator(queryset_list, 3) # Show 3 contacts per page
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	    
	context = {	"object_list" : queryset , 
			"title" : "List",
			"page_request_var" : page_request_var,
			"today" : today }

#	if request.user.is_authenticated:
#		context = { "title" : "My User List" }	
#	else:	
#		context = { "title" : "List" }
	return render(request, "post_list.html", context)	
	#return HttpResponse("<h1>List</h1>")

def post_update(request, slug=None):
	if (not request.user.is_staff) or (not request.user.is_superuser):
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Successfully <a href='#'>Edited</a>", extra_tags = 'html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
	context = { "title" : instance.title,
		     "instance" : instance,
		    "form" : form }
	#return HttpResponse("<h1>Update</h1>")
	return render(request, "post_form.html", context)

def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully Deleted")
	return redirect("Blogger:list")
	#return HttpResponse("<h1>Delete</h1>")


