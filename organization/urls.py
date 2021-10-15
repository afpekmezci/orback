from django.urls import path
from organization.views import (
	CreateOrganizationView,
	OrganizationDetailView,
	OrganizationListView,
	AddUserToOrganizationView,
	RemoveUserFromOrganization,
	OrganizationUserList,
	SupplierListView,
	OrganizationFileList,
	OrganizationFileCreate,
	OrganizationFileDetail,
	OrganizationFileUpdate,
	OrganizationFileDelete
)


file_urls = [
	path("file/list/", OrganizationFileList.as_view(), name="ListOrganizationFiles"),
	path("file/create/", OrganizationFileCreate.as_view(), name="CreateOrganizationFiles"),
	path("file/detail/<int:pk>/", OrganizationFileDetail.as_view(), name="OrganizationFileDetail"),
	path("file/update/<int:pk>/", OrganizationFileUpdate.as_view(), name="UpdateFile"),
	path("file/delete/<int:pk>/", OrganizationFileDelete.as_view(), name="DeleteFile"),
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

