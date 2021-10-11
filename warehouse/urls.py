from django.urls import path

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
]


urlpatterns = note_urls + [

]