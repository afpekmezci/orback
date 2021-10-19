from django.urls import path

from tissue.views import (
	TissueTypeListView,
	AddTissueTypeView,
	UpdateTissueTypeView,
	DeleteTissueTypeView,
	ListMaterialView,
	AddTissueMaterial,
	TissueMaterialDetail,
	UpdateTissueMaterial,
	DeleteTissueMaterial,
	TransferTissueView
)
from tissue.files_views import (
	TissueFileList,
	TissueFileCreate,
	TissueFileDetail,
	TissueFileUpdate,
	TissueFileDelete,
)

note_urls = [
     path("file/list/", TissueFileList.as_view(), name="list"),
     path("file/create/", TissueFileCreate.as_view(), name="create"),
     path("file/detail/<int:pk>/", TissueFileDetail.as_view(), name="detail"),
     path("file/update/<int:pk>/", TissueFileUpdate.as_view(), name="update"),
     path("file/delete/<int:pk>/", TissueFileDelete.as_view(), name="delete_file"),
]

material_urls = [
	path("addmaterial/", AddTissueMaterial.as_view(), name="AddTissueMaterial"),
	path("materaildetail/<int:pk>/", TissueMaterialDetail.as_view(), name="TissueMatarialDetail"),
	path("updatematerial/<int:pk>/", UpdateTissueMaterial.as_view(), name="UpdateTissueMaterial"),
	path("deletematerial/<int:pk>/", DeleteTissueMaterial.as_view(), name="DeleteTissueMaterial"),
	path("listmaterials/", ListMaterialView.as_view(), name="ListMaterialGroup"),
	path("transfer/", TransferTissueView.as_view(), name="TransferTissue"),
]

bone_type_urls = [
	path("tissuetypes/", TissueTypeListView.as_view(), name="TissueTypeList"),
	path("addtissuetype/", AddTissueTypeView.as_view(), name="AddTissueType"),
	path("updatetissuetype/<int:pk>/", UpdateTissueTypeView.as_view(), name="UpdateTissueType"),
	path("deletetissuetype/<int:pk>/", DeleteTissueTypeView.as_view(), name="DeleteTissueType"),

]

urlpatterns = note_urls + material_urls + bone_type_urls
