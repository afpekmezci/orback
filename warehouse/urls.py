from django.urls import path
from warehouse.views import CreateHospitalView, ListHospitalView, UpdateHospitalView, DeleteHospitalView


urlpatterns = [
	path('hospital/list/', ListHospitalView.as_view(), name="ListHospital"),
	path('hospital/create/', CreateHospitalView.as_view()),
	path('hospital/update/<int:pk>/', UpdateHospitalView.as_view(), name="UpdateHospital"),
	path('hospital/delete/<int:pk>/', DeleteHospitalView.as_view(), name="DeleteHospital")
]
