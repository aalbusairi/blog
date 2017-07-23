from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Post
from django.shortcuts import get_object_or_404

def home(request):
	return render(request, 'home.html', {})

def post_create(request, post_id):
	list_post = get_object_or_404(Post, id=post_id)
	context = {
		"title": "Post Page",
		"content": "Test Test Test",
		"list": list_post,
	}
	return render(request, 'post_create.html', context)	

def post_update(request):
	return render(request,	'post_update.html', {})	

def post_delete(request):
	return render(request,	'post_delete.html', {})		

def post_list(request):
	obj_list = Post.objects.all()
	context = {
	"obj_list": obj_list
	}
	return render(request,	'post_list.html', context)	

def post_detail(request):
	return render(request,	'post_detail.html', {})	
	