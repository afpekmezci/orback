from files.views import (
	FileDetailView,
	CreateFileView,
	ListFileView,
	UpdateFileView,
	DeleteFileView
)

from base.views import FilterAPIView
from organization.models import OrganizationFile, OrganizationUserFile
from organization.serializers import OrganizationFileSerializer, OrganizationUserFileSerializer
from organization.permissions import IsOwnerOrReadOnly, IsMainOrganization, IsOrgPersonelOrgMainOrg, HasOrgPermission

class OrganizationFileList(FilterAPIView):
	model = OrganizationFile
	serializer_class=OrganizationFileSerializer
	queryset = model.objects.all()
	search_fields = ['name', 'desc', 'organization__name']
	filter_fields = ['organization']
	def get_queryset(self):
		super(OrganizationFileList, self).get_queryset()
		queryset = self.queryset
		if not self.request.org.main_organization:
			queryset = self.queryset.filter(organization__exact=self.request.org)
		return queryset

class OrganizationFileCreate(CreateFileView):
	model = OrganizationFile
	serializer_class=OrganizationFileSerializer
	queryset = model.objects.all()

class OrganizationFileDetail(FileDetailView):
	model = OrganizationFile
	serializer_class=OrganizationFileSerializer
	queryset = model.objects.all()

class OrganizationFileUpdate(UpdateFileView):
	model = OrganizationFile
	serializer_class=OrganizationFileSerializer
	queryset = model.objects.all()

class OrganizationFileDelete(DeleteFileView):
	model = OrganizationFile
	serializer_class=OrganizationFileSerializer
	queryset = model.objects.all()




class OrganizationUserFileList(FilterAPIView):
	model = OrganizationUserFile
	serializer_class=OrganizationUserFileSerializer
	queryset = model.objects.all()
	search_fields = ['name', 'desc', 'organization__name']
	filter_fields = ['organization']
	def get_queryset(self):
		super(OrganizationUserFileList, self).get_queryset()
		queryset = self.queryset
		if not self.request.org.main_organization:
			queryset = self.queryset.filter(organization__exact=self.request.org)
		return queryset

class OrganizationUserFileCreate(CreateFileView):
	model = OrganizationUserFile
	serializer_class=OrganizationUserFileSerializer
	queryset = model.objects.all()

class OrganizationUserFileDetail(FileDetailView):
	model = OrganizationUserFile
	serializer_class=OrganizationUserFileSerializer
	queryset = model.objects.all()

class OrganizationUserFileUpdate(UpdateFileView):
	model = OrganizationUserFile
	serializer_class=OrganizationUserFileSerializer
	queryset = model.objects.all()

class OrganizationUserFileDelete(DeleteFileView):
	model = OrganizationUserFile
	serializer_class=OrganizationUserFileSerializer
	queryset = model.objects.all()

