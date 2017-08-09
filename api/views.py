from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from posts.models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer, CommentListSerializer, CommentCreateSerializer, UserDetailSerializer, UserCreateSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import AuthorOrStaff
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from django_comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils import timezone


class PostListAPIView(ListAPIView):
	serializer_class = PostListSerializer
	permission_classes = [AllowAny]
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['title', 'content', 'author__first_name', 'author__last_name']

	def get_queryset(self, *args, **kwargs):
		queryset_list = Post.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(author__first_name__icontains=query)|
				Q(author__last_name__icontains=query)
				).distinct()
		return queryset_list


class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	permission_classes = [AllowAny]
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	permission_classes = [IsAuthenticated, IsAdminUser]
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'

class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateSerializer
	permission_classes = [IsAuthenticated, IsAdminUser]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateSerializer
	permission_classes = [IsAuthenticated, IsAdminUser]
	lookup_field = 'slug'
	lookup_url_kwarg = 'post_slug'	

class CommentListAPIView(ListAPIView):
	serializer_class = CommentListSerializer
	permission_classes = [AllowAny]

	def get_queryset(self, *args, **kwargs):
		queryset_list = Comment.objects.all()
		query = self.request.GET.get("q")
		if query:
			queryset_list = queryset_list.filter(
				Q(object_pk=query)|
				Q(user=query)
				).distinct()
		return queryset_list

class CommentCreateAPIView(CreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentCreateSerializer
	permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):
		serializer.save(
				content_type=ContentType.objects.get_for_model(Post),
				site=Site.objects.get(id=1),
				user = self.request.user,
				user_name = self.request.user.username,
				submit_date = timezone.now()
			)		

class UserCreateAPIView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserCreateSerializer


