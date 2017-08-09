from rest_framework.permissions import BasePermission
from django.utils import timezone

class AuthorOrStaff(BasePermission):
	message = "You must be the author of this post."

	def has_object_permission(self, request, view, obj):
		date = timezone.now().date()
		if obj.publish > date or obj.draft:
			if not request.user.is_superuser or request.user.is_staff or (obj.author == request.user):
				return False
			return True 

