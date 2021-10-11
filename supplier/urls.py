from django.urls import path
from supplier.views import (
	AddSupplierView,
	ListSupplierView
)

from note.viewsets import (
	NoteListView,
	NoteCreateView,
	NoteDetailView,
	NoteUpdateViewSet
)

note_urls = [
     path("note/list/", NoteListView.as_view(), name="list"),
     path("note/create/", NoteCreateView.as_view(), name="create"),
     path("note/detail/<int:id>/", NoteDetailView.as_view(), name="detail"),
     path("note/update/<int:id>/", NoteUpdateViewSet.as_view(), name="update"),

	path("file/list/", NoteListView.as_view(is_file=True), name="list"),
	path("file/create/", NoteCreateView.as_view(is_file=True), name="create"),
	path("file/detail/<int:id>/", NoteDetailView.as_view(is_file=True), name="detail"),
	path("file/update/<int:id>/", NoteUpdateViewSet.as_view(is_file=True), name="update"),
]


urlpatterns = note_urls + [
	path('list/', ListSupplierView.as_view(), name="organization_list"),
    path('add/', AddSupplierView.as_view(), name="add_organization"),
]