from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


def contenttype_app_label_validator(app_label):
    # app label gerçekten var mı onu kontrol eder
    if not ContentType.objects.filter(app_label=app_label).exists():
        raise serializers.ValidationError(
            "This field must be an app_label from content types."
        )


def contenttype_model_name_validator(model_name):
    """model name gerçekten var mı  onu kontrol eder."""
    if not ContentType.objects.filter(model=model_name).exists():
        raise serializers.ValidationError(
            "This field must be an model_name from content types."
        )
