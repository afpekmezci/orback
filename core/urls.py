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

admin_url = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]

token_urls = [
    path('api/token/', TokenObtainPairPatchedView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshPatchedViewForWeb.as_view(), name='token_refresh'),
    path('api/token/refresh2/', TokenRefreshView.as_view(), name='token_refresh_view'),
]

modul_urls = [
    path('api/user/', include('customuser.urls')),
    path('api/organization/', include('organization.urls')),
    path('api/supplier/', include('supplier.urls')),
]

urlpatterns = admin_url + token_urls + modul_urls