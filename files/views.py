from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import GenericAPIView, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from base.views import FilterAPIView, PatchAPIView
from organization.permissions import IsOwnerOrReadOnly, IsMainOrganization, IsOrgPersonelOrgMainOrg, HasOrgPermission
from files.models import BaseFileModel
from files.serializers import BaseFileSerializer
from rest_framework.views import  APIView
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import mimetypes
import urllib

class FileDetailView(mixins.RetrieveModelMixin,
                      GenericAPIView):
	model = None
	queryset = None

	permission_classes = (HasOrgPermission, )
	serializer_class = BaseFileSerializer

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def get_serializer_context(self):
		return {
			'request': self.request,
			'format': self.format_kwarg,
			'view': self,
			'detail': True
		}
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response
from rest_framework import status
class FileServe(APIView):
	permission_classes = [AllowAny]
	def get(self, request, filename):
		"""
		 File Preview İçin Static olarak dosyaları servis eder.
		 Güvenlik için Sadece google docs üzerinden gelen istekleri yanıtlar.
		"""
		if not 'google' in request._request.environ.get('HTTP_USER_AGENT'):
			return Response(status=status.HTTP_404_NOT_FOUND)
		path = f"images/{filename}"
		short_report = open(path, 'rb')
		url = urllib.request.pathname2url(path)
		mime_type = mimetypes.guess_type(url)[0]
		response = HttpResponse(FileWrapper(short_report), content_type=mime_type)
		return response

class CreateFileView(generics.CreateAPIView):
	model = None
	queryset = None
	permission_classes = (HasOrgPermission, )
	serializer_class = BaseFileSerializer

class ListFileView(FilterAPIView):
	model = None
	queryset = None
	permission_classes = (HasOrgPermission,)
	serializer_class = BaseFileSerializer
	search_fields = ['title', 'desc']


class UpdateFileView(PatchAPIView):
	model = None
	queryset = None
	permission_classes = (HasOrgPermission, )
	serializer_class = BaseFileSerializer


class DeleteFileView(generics.DestroyAPIView):
	model = None
	queryset = None

	permission_classes = (HasOrgPermission,)
	serializer_class = BaseFileSerializer

	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.save()
