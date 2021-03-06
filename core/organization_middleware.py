from organization.models import Organization, OrganizationUser
from datetime import datetime
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthenticationFailed
from django.core.exceptions import PermissionDenied
from core import settings
from organization.utils import get_main_org
from django.contrib.auth.mixins import PermissionRequiredMixin

class OrganizationDetailMiddleware:
	"""
	Gelen Header'dan organizasyon id bilgisini ayrıştırarak;
	firma ve işlemi yapan personel ile ilgili bilgileri request nesnesine gömer.
	(eski versiyonu firma.utils -> get_organization_details fonksiyonudur.
	"""
	def __init__(self, get_response):
		self.get_response = get_response

	def get_organization_info_from_header(self, request):
		# 1. Gelen Request'in header'inden Organizasyon Bilgisi Alınır.
		try:
			orginfo = request.headers["Organization"].split("ORG")  # ORG1 şeklide bir verinin gelmesi beklenir.
			if len(orginfo) < 2:
				raise _header_error
			org_id = orginfo[1]
		except:
			org_id = None
		if org_id:
			try:
				org_id = int(org_id)
			except ValueError:
				return None

		# 2. Header'dan gelen organizasyon id'si ile, organizasyon bulunur.
		org = None
		if settings.DEBUG and request.user.is_staff:
			org = get_main_org()
		elif settings.DEBUG and request.user.is_staff is False and org_id is None:
			org = Organization.objects.filter(user_organizatons__user__in=[request.user]).first()
		else:
			if request.user:
				try:
					org = Organization.objects.filter(user_organizatons__user__in=[request.user]).get(id__exact=org_id)
				except Organization.DoesNotExist:
					raise PermissionDenied('ORG HEADER ERROR')
		request.org = org

	def get_organization_user(self, request):
		org_user = None
		if hasattr(request, 'org') and hasattr(request, 'user'):
			if request.user.is_authenticated and request.org and request.user:
				try:
					org_user = (
						OrganizationUser.objects.filter(organization_id__exact=request.org)
							.filter(is_active=True)
							.get(user=request.user)
					)
				except OrganizationUser.DoesNotExist:
					pass
		request.org_user = org_user

	@staticmethod
	def get_jwt_user(request):
		user = get_user(request)
		if user.is_authenticated:
			return user
		jwt_authentication = JWTAuthentication()
		try:
			if jwt_authentication.authenticate(request):
				user, jwt = jwt_authentication.authenticate(request)
		except AuthenticationFailed:
			pass

		return user
	def __call__(self, request):
		# Code to be executed for each request before
		# the view (and later middleware) are called.
		request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

		if request.user and request.user.is_authenticated:
			self.get_organization_info_from_header(request)
			self.get_organization_user(request)
		else:
			request.org = None
			request.org_user = None
			request.kullanim = None
		response = self.get_response(request)

		# Code to be executed for each request/response after
		# the view is called.

		return response
