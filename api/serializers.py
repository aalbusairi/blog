from rest_framework import serializers
from posts.models import Post
from django_comments.models import Comment
from django.contrib.auth.models import User

class UserDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name']

class PostListSerializer(serializers.ModelSerializer):
	detail = serializers.HyperlinkedIdentityField(
		view_name = "api:detail",
		lookup_field = "slug",
		lookup_url_kwarg = "post_slug"
		)
	class Meta:
		model = Post
		fields = ['title','content','publish', 'detail']

class PostDetailSerializer(serializers.ModelSerializer):
	author = UserDetailSerializer()
	comments = serializers.SerializerMethodField()

	class Meta:
		model = Post
		fields = ['id','author','title', 'slug', 'content','publish','draft', 'image', 'comments']

	def get_comments(self, obj):
		comment_queryset = Comment.objects.filter(object_pk=obj.id)
		comments = CommentListSerializer(comment_queryset, many=True).data
		return comments

class PostCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ['title', 'content','publish','draft']	

class CommentListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['content_type', 'object_pk','user','comment','submit_date']


class CommentCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['object_pk','comment']

class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = User
		fields = ['username', 'password']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.save()
		return validated_data		

