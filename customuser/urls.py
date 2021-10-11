from django.urls import path
from customuser.views import (
	UserDetailView,
	ForgetPasswordView,
	ResetPasswordView,
	ChangePasswordView
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


urlpatterns = [
	path("", UserDetailView.as_view(), name="user_detail"),
	path("forget/", ForgetPasswordView.as_view(), name="ForgetRequet"),
	path("reset/", ResetPasswordView.as_view(), name="ResetPassword"),
	path("change/", ChangePasswordView.as_view(), name="ChangePassword"),
]