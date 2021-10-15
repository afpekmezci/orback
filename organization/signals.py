from django.db.models.signals import post_save
from django.dispatch import receiver
from organization.models import Organization
from core.get_request import current_request
from warehouse.models import Warehouse
from organization.utils import get_main_org

@receiver(post_save, sender=Organization)
def self_warehouse(sender, instance, raw, **kwargs):
	if kwargs.get('created'):

		try:
			Warehouse.objects.create(name=f'{instance.name} Merkez Depo', city=instance.city, organization=instance)
		except Exception as exp:
			print('SELF WAREHOSE CREATE ERROR', exp)
