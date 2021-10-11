from rest_framework.generics import GenericAPIView, mixins
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

class FilterAPIView(mixins.ListModelMixin, GenericAPIView):

	def post(self, request, *args, **kwargs):
		self.queryset = self.queryset.filter(is_active=True)
		_f = {}
		if self.request.data.get('filter'):
			for filter_key, filter_value in self.request.data.get('filter').items():
				for model_key in self.model._meta.fields:
					if model_key.name == filter_key and filter_value:
						_f[model_key.name] = filter_value
		_search = Q()
		if hasattr(self, 'search_fields') and self.search_fields and self.request.data.get('search'):
			for item in self.search_fields:
				_search &= Q(**{"%s__icontains" % item: self.request.data.get('search')})
			self.queryset = self.queryset.filter(_search)
		self.queryset = self.queryset.filter(**_f)

		if not self.queryset:
			return Response(status=status.HTTP_204_NO_CONTENT)
		return self.list(request, *args, **kwargs)



class EnablePartialUpdateMixin:
	"""
		Enable partial updates
	"""

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
