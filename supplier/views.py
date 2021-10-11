from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from base.views import FilterAPIView

from supplier.models import Supplier
from supplier.serializers import SupplierSerializer


class ListSupplierView(FilterAPIView):
	permission_classes = [IsAuthenticated]
	model = Supplier
	queryset = Supplier.objects.all()
	serializer_class = SupplierSerializer
	search_fields = ['company__name']

class AddSupplierView(generics.CreateAPIView):

	permission_classes = [IsAuthenticated]
	model = Supplier
	queryset = Supplier.objects.none()
	serializer_class = SupplierSerializer