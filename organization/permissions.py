from rest_framework import permissions
from organization.models import Organization

class HasOrgPermission(permissions.BasePermission):

	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated and request.org)

class IsOwnerOrReadOnly(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

		# Only Organization Owner Can Do
		return request.org.main_organization or obj.is_owner(request.user)

class IsMainOrganization(permissions.BasePermission):

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True

		# Only Main Organizaiton Can Do
		return request.org.main_organization


class IsOrgPersonelOrgMainOrg(permissions.BasePermission):

	def has_object_permission(self, request, view, obj):

		return request.org.main_organization or obj.is_employee(request.user)
