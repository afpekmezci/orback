from core.utils import ImageUtils
from django.core.files.base import ContentFile
import base64
import six
import uuid
import imghdr
import mimetypes
from rest_framework import serializers
from core.settings import API_URL
class Base64FileField(serializers.FileField):

	def to_representation(self, value):
		super(Base64FileField, self).to_representation(value)
		if self.context.get('detail'):
			try:
				return ImageUtils().GetImageFileToBase64(value)
			except Exception:
				raise OSError("Error encoding file")
		else:
			return f"{API_URL}staticfile{value.url}"

	def to_internal_value(self, data):


		if isinstance(data, six.string_types):
			file_extension = self.get_file_extension(data)
			if 'data:' in data and ';base64,' in data:
				header, data = data.split(';base64,')

			try:
				decoded_file = base64.b64decode(data)
			except TypeError:
				self.fail('invalid_image')

			file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
			complete_file_name = "%s%s" % (file_name, file_extension, )
			data = ContentFile(decoded_file, name=complete_file_name)

		return super(Base64FileField, self).to_internal_value(data)

	def get_file_extension(self, base64_data):
		return mimetypes.guess_extension(mimetypes.guess_type(base64_data)[0])