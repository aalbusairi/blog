from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import PostForm
from django.contrib import messages

def home(request):
	return render(request, 'home.html', {})

def post_create(request):
	form = PostForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, "Post Succesfully Created")
		return redirect("posts:list")
	context = {
	"form": form
	}
	return render(request, 'post_create.html', context)	

def post_update(request, post_id):
	post_object = get_object_or_404(Post, id=post_id)
	form = PostForm(request.POST or None, instance=post_object)
	if form.is_valid():
		form.save()
		messages.success(request, "Post Succesfully Updated")
		return redirect("posts:list")
	context = {
	"form":form,
	"post_object":post_object,
	}
	return render(request,	'post_update.html', context)	

def post_delete(request, post_id):
	post_object = get_object_or_404(Post, id=post_id)
	post_object.delete()
	messages.warning(request, "Post Deleted")
	return redirect("posts:list")
	return render(request,	'post_delete.html', {})		

def post_list(request):
	obj_list = Post.objects.all()
	context = {
	"obj_list": obj_list
	}
	return render(request,	'post_list.html', context)	

def post_detail(request, post_id):
	list_post = get_object_or_404(Post, id=post_id)
	context = {
		"title": "Post Page",
		"content": "Test Test Test",
		"list": list_post,
	}	
	return render(request,	'post_detail.html', context)	
	