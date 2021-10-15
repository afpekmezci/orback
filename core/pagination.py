from rest_framework.pagination import BasePagination, _positive_int, _divide_with_ceil, _get_displayed_page_numbers, _get_page_links, _reverse_ordering
from base64 import b64decode, b64encode
from collections import OrderedDict, namedtuple
from urllib import parse

from django.core.paginator import InvalidPage
from django.core.paginator import Paginator as DjangoPaginator
from django.template import loader
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from rest_framework.compat import coreapi, coreschema
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.utils.urls import remove_query_param, replace_query_param


Cursor = namedtuple('Cursor', ['offset', 'reverse', 'position'])
PageLink = namedtuple('PageLink', ['url', 'number', 'is_active', 'is_break'])

PAGE_BREAK = PageLink(url=None, number=None, is_active=False, is_break=True)


class CountPostPagination(BasePagination):
	"""
	A simple page number based style that supports page numbers as post request parameters. For example:
	http://api.example.org/organization/list/
	request_body: {page : 0, count: 20}
	"""
	page_size = api_settings.PAGE_SIZE
	django_paginator_class = DjangoPaginator
	page_query_param = 'page'
	page_query_description = _('A page number within the paginated result set.')
	page_size_query_param = 'count'
	page_size_query_description = _('Number of results to return per page.')
	max_page_size = None

	last_page_strings = ('last',)

	template = 'rest_framework/pagination/numbers.html'

	invalid_page_message = _('Invalid page.')

	def paginate_queryset(self, queryset, request, view=None):
		"""
		Paginate a queryset if required, either returning a
		page object, or `None` if pagination is not configured for this view.
		"""
		page_size = self.get_page_size(request)
		if not page_size:
			return None

		paginator = self.django_paginator_class(queryset, page_size)
		page_number = request.data.get(self.page_query_param, 1)
		print('PAGE NUMBER : ', page_number)
		if page_number in self.last_page_strings:
			page_number = paginator.num_pages

		try:
			self.page = paginator.page(page_number)
		except InvalidPage as exc:
			msg = self.invalid_page_message.format(
				page_number=page_number, message=str(exc)
			)
			raise NotFound(msg)

		if paginator.num_pages > 1 and self.template is not None:
			# The browsable API should display pagination controls.
			self.display_page_controls = True

		self.request = request
		return list(self.page)

	def get_paginated_response(self, data):
		return Response(OrderedDict([
			('count', self.page.paginator.count),
			('results', data)
		]))

	def get_paginated_response_schema(self, schema):
		return {
			'type': 'object',
			'properties': {
				'count': {
					'type': 'integer',
					'example': 123,
				},
				'current_page': page_number,
				'results': schema,
			},
		}

	def get_page_size(self, request):
		if self.page_size_query_param:
			try:
				return _positive_int(
					request.data.get(self.page_size_query_param, self.page_size),
					strict=True,
					cutoff=self.max_page_size
				)
			except (KeyError, ValueError):
				pass

		return self.page_size

	def to_html(self):
		template = loader.get_template(self.template)
		context = self.get_html_context()
		return template.render(context)

	def get_html_context(self):
		base_url = self.request.build_absolute_uri()

		def page_number_to_url(page_number):
			if page_number == 1:
				return remove_query_param(base_url, self.page_query_param)
			else:
				return replace_query_param(base_url, self.page_query_param, page_number)

		current = self.page.number
		final = self.page.paginator.num_pages
		page_numbers = _get_displayed_page_numbers(current, final)
		page_links = _get_page_links(page_numbers, current, page_number_to_url)

		return {
			'page_links': page_links
		}

	def get_schema_fields(self, view):
		assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
		assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
		fields = [
			coreapi.Field(
				name=self.page_query_param,
				required=False,
				location='query',
				schema=coreschema.Integer(
					title='Page',
					description=force_str(self.page_query_description)
				)
			)
		]
		if self.page_size_query_param is not None:
			fields.append(
				coreapi.Field(
					name=self.page_size_query_param,
					required=False,
					location='query',
					schema=coreschema.Integer(
						title='Page size',
						description=force_str(self.page_size_query_description)
					)
				)
			)
		return fields

	def get_schema_operation_parameters(self, view):
		parameters = [
			{
				'name': self.page_query_param,
				'required': False,
				'in': 'query',
				'description': force_str(self.page_query_description),
				'schema': {
					'type': 'integer',
				},
			},
		]
		if self.page_size_query_param is not None:
			parameters.append(
				{
					'name': self.page_size_query_param,
					'required': False,
					'in': 'query',
					'description': force_str(self.page_size_query_description),
					'schema': {
						'type': 'integer',
					},
				},
			)
		return parameters

