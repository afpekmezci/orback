from files.views import (FileDetailView, CreateFileView, ListFileView, UpdateFileView, DeleteFileView,)
from tissue.models import TissueFile
from tissue.serializers import TissueFileSerializer
from base.views import FilterAPIView

class TissueFileList(FilterAPIView):
	model = TissueFile
	serializer_class=TissueFileSerializer
	queryset = model.objects.all()
	search_fields = ['name', 'desc', 'tissue__patient', 'tissue__hospital__name']
	filter_fields = ['tissue']
	def get_queryset(self):
		super(TissueFileList	, self).get_queryset()
		queryset = self.queryset
		if not self.request.org.main_organization:
			queryset = self.queryset.filter(tissue__organization__exact=self.request.org)
		return queryset

class TissueFileCreate(CreateFileView):
	model = TissueFile
	serializer_class=TissueFileSerializer
	queryset = model.objects.all()

class TissueFileDetail(FileDetailView):
	model = TissueFile
	serializer_class=TissueFileSerializer
	queryset = model.objects.all()

class TissueFileUpdate(UpdateFileView):
	model = TissueFile
	serializer_class=TissueFileSerializer
	queryset = model.objects.all()

class TissueFileDelete(DeleteFileView):
	model = TissueFile
	serializer_class=TissueFileSerializer
	queryset = model.objects.all()
