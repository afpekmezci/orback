from django.urls import path

from note.viewsets import (
	NoteListView,
	NoteCreateView,
	NoteDetailView,
	NoteUpdateViewSet
)
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
)


note_urls = [
     path("note/list/", NoteListView.as_view(), name="list"),
     path("note/create/", NoteCreateView.as_view(), name="create"),
     path("note/detail/<int:id>/", NoteDetailView.as_view(), name="detail"),
     path("note/update/<int:id>/", NoteUpdateViewSet.as_view(), name="update"),
]

material_urls = [
	path("addmaterial/", AddTissueMaterial.as_view(), name="AddTissueMaterial"),
	path("materaildetail/<int:pk>/", TissueMaterialDetail.as_view(), name="TissueMatarialDetail"),
	path("updatematerial/<int:pk>/", UpdateTissueMaterial.as_view(), name="UpdateTissueMaterial"),
	path("deletematerial/<int:pk>/", DeleteTissueMaterial.as_view(), name="DeleteTissueMaterial"),
	path("listmaterials/", ListMaterialView.as_view(), name="ListMaterialGroup"),
]

bone_type_urls = [
	path("tissuetypes/", TissueTypeListView.as_view(), name="TissueTypeList"),
	path("addtissuetype/", AddTissueTypeView.as_view(), name="AddTissueType"),
	path("updatetissuetype/<int:pk>/", UpdateTissueTypeView.as_view(), name="UpdateTissueType"),
	path("deletetissuetype/<int:pk>/", DeleteTissueTypeView.as_view(), name="DeleteTissueType"),

]

urlpatterns = note_urls + material_urls + bone_type_urls
