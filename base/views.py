from rest_framework.generics import GenericAPIView, mixins
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from django.db.models.functions import Lower
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.pagination import LimitOffsetPagination


def get_annotation(key):

	lower_key = f"lower_{key}"
	return {lower_key: Lower(key)}


class FilterAPIView(mixins.ListModelMixin, GenericAPIView):

	def post(self, request, *args, **kwargs):

		self.queryset = self.queryset.filter(is_active=True)

		_filter = Q()

		for filter_fields, filter_value in self.request.data.get('filter', {}).items():

			for model_key in self.model._meta.fields:
				if model_key.name == filter_fields and filter_value:
					if isinstance(filter_value, list):
						_filter &= Q(**{"%s__in" % model_key.name: filter_value})
					else:
						_filter &= Q(**{"%s" % model_key.name: filter_value})

		_search = Q()

		if hasattr(self, 'search_fields') and self.search_fields and self.request.data.get('search'):
			for item in self.search_fields:
				self.queryset = self.queryset.annotate(**get_annotation(item))
				_search |= Q(**{"lower_%s__contains" % item: self.request.data.get('search')})
			self.queryset = self.queryset.filter(_search)

		self.queryset = self.queryset.filter(_filter)

		if not self.queryset:
			return Response(status=status.HTTP_404_NOT_FOUND)
		return self.list(request, *args, **kwargs)

class EnablePartialUpdateMixin:
	""" Enable partial updates """

	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)

		if getattr(instance, '_prefetched_objects_cache', None):
			instance._prefetched_objects_cache = {}

		return Response(serializer.data)

	def perform_update(self, serializer):
		serializer.save()

	def patch(self, request, *args, **kwargs):
		kwargs['partial'] = True
		return super().update(request, *args, **kwargs)


class PatchAPIView(EnablePartialUpdateMixin,
					GenericAPIView):
	"""
	Concrete view for updating a model instance.
	"""
	def patch(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)


class DeleteAPIView(mixins.DestroyModelMixin, GenericAPIView):

	def perform_destroy(self, instance):
		instance.is_active = False
		instance.save()