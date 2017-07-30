from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import PostForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote



def post_create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request, "Post Succesfully Created")
		return redirect("posts:list")
	context = {
	"form": form,
	}
	return render(request, 'post_create.html', context)	

def post_update(request, slug):
	post_object = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=post_object)
	if form.is_valid():
		form.save()
		messages.success(request, "Post Succesfully Updated")
		return redirect("posts:list")
	context = {
	"form":form,
	"post_object":post_object,
	}
	return render(request,	'post_update.html', context)	

def post_delete(request, slug):
	post_object = get_object_or_404(Post, slug=slug)
	post_object.delete()
	messages.warning(request, "Post Deleted")
	return redirect("posts:list")
	return render(request,	'post_delete.html', {})		

def post_list(request):
	obj_list = Post.objects.all()#.order_by("-timestamp","-updated")
	paginator = Paginator(obj_list, 4) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		obj = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		obj = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		obj = paginator.page(paginator.num_pages)

	context = {
	"obj_list": obj
	}
	return render(request,	'post_list.html', context)	

def post_detail(request, slug):
	list_post = get_object_or_404(Post, slug=slug)
	context = {
		"title": "Post Page",
		"content": "Test Test Test",
		"list": list_post,
	}	
	return render(request,	'post_detail.html', context)	
	