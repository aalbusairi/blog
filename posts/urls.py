from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/$', views.post_create, name="create"),
	url(r'^update/(?P<slug>[-\w]+)/$', views.post_update, name="update"),
	url(r'^delete/(?P<slug>[-\w]+)/$', views.post_delete, name="delete"),
	url(r'^list/$', views.post_list, name="list"),
	url(r'^detail/(?P<slug>[-\w]+)/$', views.post_detail, name="detail"),
	url(r'^signup/$', views.usersignup, name="signup"),
	url(r'^login/$', views.userlogin, name="login"),
	url(r'^logout/$', views.userlogout, name="logout"),
	url(r'^ajax_like/(?P<post_id>\d+)/$', views.ajax_like, name="like_button"),
]
