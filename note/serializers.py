from rest_framework import serializers

from core.utils import ImageUtils
from note.fields import Base64ImageField
from note.models import Note
from note.validator import (
    contenttype_app_label_validator,
    contenttype_model_name_validator,
)
import base64

class NoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    app_label = serializers.CharField(
        max_length=50, validators=[contenttype_app_label_validator]
    )
    model_name = serializers.CharField(
        max_length=50, validators=[contenttype_model_name_validator]
    )
    file = Base64ImageField(
        represent_in_base64=True, required=False
    )  # base64 olan datayı dosya olarak dönderir ve represe ederken base64 olarak sunar
    # base64 olarak sunmasını isteniyor ise represent_in_base64 = True yazılması gerekir.
    can_edit = serializers.SerializerMethodField(read_only=True, required=False)

    def get_thumbnail(self, obj):
        return None
    def get_can_edit(self, obj):
        req = self.context.get('request', None)
        if req:
            if req.org_user == obj.created_by_id:
                return True
        return False
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get("detay"):
            pass
        else:
            _th = data['thumbnail']
            data.pop('thumbnail')
            data['file'] = _th

        _user_image = None
        if instance.created_by_id.user.person_thumbnail:
            data['user_image'] = ImageUtils().GetImageFileToBase64(instance.created_by_id.user.person_thumbnail)
        return data


    def get_created_by_name(self, obj):
        return obj.created_by_id.user.get_full_name()

    def create(self, validated_data):
        req = self.context.get('request')
        validated_data["created_by_id"] = req.org_user
        validated_data["content_object"] = self.Meta.model.get_content_object(
            app_label=validated_data.pop("app_label"),
            model_name=validated_data.pop("model_name"),
            object_id=validated_data.pop("object_id"),
        )
        print('VALIDATED DATA : ', validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        req = self.context.get('request')
        if instance.created_by_id != req.org_user:
            raise serializers.ValidationError('cant edit')
        instance.content_object = self.Meta.model.get_content_object(
            app_label=validated_data.pop("app_label"),
            model_name=validated_data.pop("model_name"),
            object_id=validated_data.pop("object_id"),
        )
        return super().update(instance, validated_data)

    class Meta:
        model = Note
        fields = [
            "id",
            "app_label",
            "model_name",
            "object_id",
            "created_by_name",
            "created_by_id",
            "title",
            "note",
            "is_public",
            "file",
            "created_time",
            "can_edit",
            "pin",
            "is_deleted",
            "show_status"
        ]
        read_only_fields = [
            "created_by_id",
            "created_by_name",
            "created_time",
        ]
        write_only_fields = [
            "is_deleted"
        ]
