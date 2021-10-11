from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.utils import ImageUtils

from note.models import Note
