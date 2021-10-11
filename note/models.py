from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from organization.models import OrganizationUser
from customuser.models import User
from base.models import BaseModel
from core.utils import get_upload_path


class NoteManager(models.Manager):
    def get_queryset(self):
        return super(NoteManager, self).get_queryset().filter(is_deleted=False).order_by('-created_time')

class Note(BaseModel):
    # Usage;
    # Note.objects.create(
    #     created_by_id=org_user,
    #     content_object=Note.get_content_object(
    #         app_label:str,
    #         model_name:str,
    #         object_id:int
    #     ),
    #     note="custom note", title="note title"
    # )

    herkes = "Herkes Görebilir"
    sirket = "Şirket İçi"
    kendim = "Kendim"

    public_choices = (
        (1, herkes), (2, sirket), (3, kendim)
    )
    created_by_id = models.ForeignKey(
        OrganizationUser,
        on_delete=models.PROTECT,
        related_name="note_created_by",
        verbose_name="OluşturanId",
    )
    title = models.CharField(max_length=256, blank=True, null=True)
    note = models.CharField(
        verbose_name="Note Detail", max_length=2048, blank=True, null=True
    )
    file = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    show_status = models.PositiveSmallIntegerField(choices=public_choices, default=2, verbose_name='Kimler Görüntüler')
    pin = models.CharField(max_length=24, verbose_name='Pin', default="#4CAF50", blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='note_content')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    objects = NoteManager()

    def model_name(self):
        return str(self.content_type.model)

    def get_object(self):  # NOTE = self.content_object
        return self.get_content_object(
            self.app_label(), self.model_name(), self.object_id
        )

    @staticmethod
    def get_content_object(app_label: str, model_name: str, object_id: int):
        return ContentType.objects.get(
            app_label=app_label, model=model_name
        ).get_object_for_this_type(id=object_id)

    def app_label(self):
        return self.content_type.app_label

    def __str__(self):
        return f"{self.id} - {self.title}, {self.model_name()}"
