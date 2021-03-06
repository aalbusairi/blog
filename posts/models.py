from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Post(models.Model):
	author = models.ForeignKey(User, default=1)
	title = models.CharField(max_length=255)
	slug = models.SlugField(unique=True, null=True)
	image = models.ImageField(upload_to="blog_images", null=True, blank=True)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"slug": self.slug})	

	class Meta:
		ordering = ['-timestamp', '-updated']

# def create_slug(instance, new_slug=None):
# 	slug=slugify(instance.title)
# 	if new_slug is not None:
# 		slug= new_slug
# 	qs = Post.objects.filter(slug=slug).order_by("-id")
# 	exists= qs.exists()
# 	if exists:
# 		new_slug = "%s-%s"%(slug, qs.first().id)
# 		return create_slug(instance, new_slug=new_slug)
# 	return slug 				

def post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		slug=slugify(instance.title)
		qs = Post.objects.filter(slug=slug).order_by("-id")
		exists= qs.exists()
		if exists:
			slug = "%s-%s"%(slug, instance.id)
		instance.slug = slug
		instance.save()

post_save.connect(post_receiver, sender=Post)	

class Like(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	created = models.DateTimeField(auto_now_add=True)		

