from rest_framework import permissions
from organization.models import Organization
from base.utils import can_edit


class TissueMaterialPermission(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		return can_edit(obj, request)
