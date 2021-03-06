from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404
from .forms import PostForm, UserSignup, UserLogin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

def usersignup(request):
	context = {}
	form = UserSignup()
	context['form'] = form
	if request.method == 'POST':
		form = UserSignup(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = user.username
			password = user.password

			user.set_password(password)
			user.save()

			auth_user = authenticate(username=username, password=password)
			login(request, auth_user)

			return redirect("posts:list")
		messages.warning(request, form.errors)
		return redirect("posts:signup")
	return render(request, 'signup.html', context)

def userlogin(request):
	context = {}
	form = UserLogin()
	context['form'] = form
	if request.method == 'POST':
		form = UserLogin(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('posts:list')

			messages.warning(request, "Wrong username/password combination. Please try again.")
			return redirect("posts:login")
		messages.warning(request, form.errors)
		return redirect("posts:login")
	return render(request, 'login.html', context)

def userlogout(request):
    logout(request)
    return redirect("posts:login")	
			
def post_create(request):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit = False)
		obj.author = request.user
		obj.save()
		messages.success(request, "Post Succesfully Created")
		return redirect("posts:list")
	context = {
	"form": form,
	}
	return render(request, 'post_create.html', context)	

def post_update(request, slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
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
	if not (request.user.is_superuser):
		raise Http404
	post_object = get_object_or_404(Post, slug=slug)
	post_object.delete()
	messages.warning(request, "Post Deleted")
	return redirect("posts:list")
	return render(request,	'post_delete.html', {})		

def post_list(request):
	today = timezone.now().date()

	if request.user.is_superuser or request.user.is_staff:
		obj_list = Post.objects.all()
	else:
		obj_list = Post.objects.filter(draft=False).filter(publish__lte=today)

	query = request.GET.get("q")
	if query:
		obj_list = obj_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)
			).distinct()

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
	"obj_list": obj,
	"today": today,
	}
	return render(request,	'post_list.html', context)	

def post_detail(request, slug):
	list_post = get_object_or_404(Post, slug=slug)
	date = timezone.now().date()
	if list_post.publish > date or list_post.draft:
		if not (request.user.is_superuser or request.user.is_staff):
			raise Http404
	if request.user.is_authenticated():
		if Like.objects.filter(post=list_post, user=request.user).exists():
			liked = True
		else:
			liked = False
	post_like_count = list_post.like_set.all().count()
						
	context = {
		"list": list_post,
		"like_count": post_like_count,
		# "liked": liked,
	}	
	return render(request,	'post_detail.html', context)

def ajax_like(request, post_id):
	obj = Post.objects.get(id=post_id)
	like, created = Like.objects.get_or_create(user=request.user, post=obj)

	if created:
		action="like"
	else:
		like.delete()
		action="unlike"

	post_like_count = obj.like_set.all().count()	
			
	context = {
		"action": action,
		"like_count": post_like_count,
	}

	return JsonResponse(context, safe=False)



	