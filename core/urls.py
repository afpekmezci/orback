from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from customuser.views import (
    TokenObtainPairPatchedView,
    TokenRefreshPatchedViewForWeb
)
from files.views import FileServe

from django.views.static import serve


admin_url = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('servefiles/images/<str:filename>/', FileServe.as_view()),
]

token_urls = [
    path('api/token/', TokenObtainPairPatchedView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshPatchedViewForWeb.as_view(), name='token_refresh'),
    path('api/token/refresh2/', TokenRefreshView.as_view(), name='token_refresh_view'),
]

modul_urls = [
    path('api/user/', include('customuser.urls'), name="UserModule"),
    path('api/organization/', include('organization.urls'), name="OrganizationModule"),
    path('api/warehouse/', include('warehouse.urls'), name="WarehouseModule"),
    path('api/tissue/', include('tissue.urls'), name="TissueModule"),
]

urlpatterns = admin_url + token_urls + modul_urls