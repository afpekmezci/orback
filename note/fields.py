"""# Base64ImageField field'i gelen base64 resim datasını dosya olarak
dönderir.

# ve Base64ImageField(represent_in_base64=True) represe ederken base64 olarak sunar.
#
# Base64FileField field'i gelen base64 dosya datasını dosya olarak dönderir,
# ve Base64ImageField(represent_in_base64=True) olarak ayarlanırsa represe ederken yine base64 formatında represe eder
#
# thumbnail;
#
# base64 olarak sunmasını isteniyor ise represent_in_base64 = True yazılması gerekir. ve only read içine koymak gerekir.
"""


import base64
import binascii
import imghdr
import io
import mimetypes
import uuid

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from rest_framework.fields import FileField, ImageField

from core.utils import ImageUtils

from note.models import Note

import pdb

class Base64FieldMixin:
    @property
    def ALLOWED_TYPES(self):
        return ['.pdf', '.docx', '.xlsx', '.jpg', '.jpeg', '.png','.xls', '.doc', '.txt', '.dwg', '.dxf']

    @property
    def INVALID_FILE_MESSAGE(self):
        raise NotImplementedError

    @property
    def INVALID_TYPE_MESSAGE(self):
        raise NotImplementedError

    EMPTY_VALUES = (None, "", [], (), {})

    def __init__(self, *args, **kwargs):
        self.represent_in_base64 = kwargs.pop("represent_in_base64", False)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, base64_data):
        # Check if this is a base64 string
        if base64_data in self.EMPTY_VALUES:
            return None

        if isinstance(base64_data, str):
            # Strip base64 header.
            try:
                extension = mimetypes.guess_extension(mimetypes.guess_type(base64_data)[0])
            except:
                self.INVALID_TYPE_MESSAGE()
            if ";base64," in base64_data:
                header, base64_data = base64_data.split(";base64,")

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except (TypeError, binascii.Error, ValueError):
                raise ValidationError(self.INVALID_FILE_MESSAGE)
            # Generate file name:
            file_name = self.get_file_name(decoded_file)
            # Get the file name extension:

            if self.ALLOWED_TYPES and extension not in self.ALLOWED_TYPES:
                raise ValidationError(self.INVALID_TYPE_MESSAGE)
            complete_file_name = file_name + extension
            data = ContentFile(decoded_file, name=complete_file_name)
            return super().to_internal_value(data)
        raise ValidationError(
            _(
                "Invalid type. This is not an base64 string: {}".format(
                    type(base64_data)
                )
            )
        )

    def get_file_name(self, decoded_file):
        return str(uuid.uuid4())

    def to_representation(self, file):
        if self.represent_in_base64:
            # If the underlying ImageField is blank, a ValueError would be
            # raised on `open`. When representing as base64, simply return an
            # empty base64 str rather than let the exception propagate unhandled
            # up into serializers.
            if not file:
                return None
            print('FİLE : ', file)
            try:
                return ImageUtils().GetImageFileToBase64(file)
            except Exception:
                raise OSError("Error encoding file")
        else:
            return super().to_representation(file)


class Base64ImageField(Base64FieldMixin, ImageField):
    """A django-rest-framework field for handling image-uploads through raw
    post data.

    It uses base64 for en-/decoding the contents of the file.
    """

    ALLOWED_TYPES = []
    INVALID_FILE_MESSAGE = _("Please upload a valid image.")
    INVALID_TYPE_MESSAGE = _("The type of the image couldn't be determined.")

    def get_file_extension(self, filename, decoded_file, base64_data):
        try:
            from PIL import Image
        except ImportError:
            raise ImportError("Pillow is not installed.")
        extension = imghdr.what(filename, decoded_file)
        # Try with PIL as fallback if format not detected due
        # to bug in imghdr https://bugs.python.org/issue16512
        if extension is None:
            try:
                image = Image.open(io.BytesIO(decoded_file))
            except OSError:
                raise ValidationError(self.INVALID_FILE_MESSAGE)
            extension = image.format.lower()
        return extension

    def get_file_name(self, decoded_file):
        org = self.context.get('request').org
        return f"/original/{str(org.id) + str(uuid.uuid4())}/-"


class Base64FileField(Base64FieldMixin, FileField):
    """A django-rest-framework field for handling file-uploads through raw post
    data.

    It uses base64 for en-/decoding the contents of the file.
    """

    INVALID_FILE_MESSAGE = _("Please upload a valid file.")
    INVALID_TYPE_MESSAGE = _("The type of the file couldn't be determined .")

    def get_file_extension(self, filename, decoded_file, base64_data):
        return mimetypes.guess_extension(mimetypes.guess_type(base64_data)[0])

    def get_file_name(self, decoded_file):
        org = self.context.get('request').org
        return f"/{str(org.id) + str(uuid.uuid4())}/-"
