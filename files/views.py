from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import GenericAPIView, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from base.views import FilterAPIView
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

class FileServe(APIView):
	permission_classes = [AllowAny]
	def get(self, request, filename):
		path = f"images/{filename}"
		short_report = open(path, 'rb')
		url = urllib.request.pathname2url(path)
		mime_type = mimetypes.guess_type(url)[0]
		print('MIME TYPE : ', mime_type)
		response = HttpResponse(FileWrapper(short_report), content_type=mime_type)
		return response
		return response

class CreateFileView(generics.CreateAPIView):
	permission_classes = (HasOrgPermission, )
	serializer_class = BaseFileSerializer

class ListFileView(FilterAPIView):
	permission_classes = (HasOrgPermission,)
	serializer_class = BaseFileSerializer
	search_fields = ['title', 'desc']


class UpdateFileView(generics.UpdateAPIView):
	permission_classes = (HasOrgPermission, )
	serializer_class = BaseFileSerializer


class DeleteFileView(generics.DestroyAPIView):
	permission_classes = (HasOrgPermission,)
	serializer_class = BaseFileSerializer

	def perform_destroy(self, instance):
		instance.is_deleted = True
		instance.save()
