from django.urls import path
from organization.views import (
	CreateOrganizationView,
	OrganizationDetailView,
	OrganizationListView,
	AddUserToOrganizationView,
	RemoveUserFromOrganization,
	OrganizationUserList,
	SupplierListView,
)

from organization.files_views import (
	OrganizationFileList,
	OrganizationFileCreate,
	OrganizationFileDetail,
	OrganizationFileUpdate,
	OrganizationFileDelete,

	OrganizationUserFileList,
	OrganizationUserFileCreate,
	OrganizationUserFileDetail,
	OrganizationUserFileUpdate,
	OrganizationUserFileDelete
)


file_urls = [
	path("file/list/", OrganizationFileList.as_view(), name="ListOrganizationFiles"),
	path("file/create/", OrganizationFileCreate.as_view(), name="CreateOrganizationFiles"),
	path("file/detail/<int:pk>/", OrganizationFileDetail.as_view(), name="OrganizationFileDetail"),
	path("file/update/<int:pk>/", OrganizationFileUpdate.as_view(), name="OrganizationUpdateFile"),
	path("file/delete/<int:pk>/", OrganizationFileDelete.as_view(), name="OrganizationDeleteFile"),

	path("userfile/list/", OrganizationUserFileList.as_view(), name="ListOrganizationUserFiles"),
	path("userfile/create/", OrganizationUserFileCreate.as_view(), name="CreateOrganizationUserFiles"),
	path("userfile/detail/<int:pk>/", OrganizationUserFileDetail.as_view(), name="OrganizationUserFileDetail"),
	path("userfile/update/<int:pk>/", OrganizationUserFileUpdate.as_view(), name="OrganizationUserUpdateFile"),
	path("userfile/delete/<int:pk>/", OrganizationUserFileDelete.as_view(), name="OrganizationUserDeleteFile"),
]

urlpatterns = file_urls + [
	path('list/', OrganizationListView.as_view(), name="organization_list"),
    path('add/', CreateOrganizationView.as_view(), name="add_organization"),
	path('update/<int:pk>/', OrganizationDetailView.as_view(), name="organization_update"),
	path('detail/<int:pk>/', OrganizationDetailView.as_view(), name="organization_detail"),
	path('delete/<int:pk>/', OrganizationDetailView.as_view(), name="delete_organization"),
	path('adduser/', AddUserToOrganizationView.as_view(), name="add_organization_user"),
	path('removeuser/<int:pk>/', RemoveUserFromOrganization.as_view(), name="remove_user"),
	path('userlist/', OrganizationUserList.as_view(), name="organization_user_list"),
	path('supplier/', SupplierListView.as_view(), name="SupplierList"),
]

