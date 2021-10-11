from django.urls import path
from organization.views import (
	CreateOrganizationView,
	OrganizationDetailView,
	OrganizationListView,
	AddUserToOrganizationView,
	RemoveUserFromOrganization,
	OrganizationUserList
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
	path('list/', OrganizationListView.as_view(), name="organization_list"),
    path('add/', CreateOrganizationView.as_view(), name="add_organization"),
	path('update/<int:pk>/', OrganizationDetailView.as_view(), name="organization_update"),
	path('detail/<int:pk>/', OrganizationDetailView.as_view(), name="organization_detail"),
	path('delete/<int:pk>/', OrganizationDetailView.as_view(), name="delete_organization"),
	path('adduser/', AddUserToOrganizationView.as_view(), name="add_organization_user"),
	path('removeuser/<int:pk>/', RemoveUserFromOrganization.as_view(), name="remove_user"),
	path('userlist/', OrganizationUserList.as_view(), name="organization_user_list"),
]

