from django.db.models.signals import post_save
from django.dispatch import receiver
from organization.models import Organization
from supplier.models import Supplier
from core.get_request import current_request
from warehouse.models import Warehouse
@receiver(post_save, sender=Organization)
def self_supplier(sender, instance, raw, **kwargs):
	if kwargs.get('created'):
		try:
			Supplier.objects.create(employer=current_request().org, supplier=instance, created_by=current_request().user)
		except Exception as exp:
			print('SELF SUPPLIER CREATE ERROR', exp)

@receiver(post_save, sender=Organization)
def self_warehouse(sender, instance, raw, **kwargs):
	if kwargs.get('created'):
		try:
			Warehouse.objects.create(name=f'{instance.name} Merkez Depo', city=instance.city, organization=instance)
		except Exception as exp:
			print('SELF WAREHOSE CREATE ERROR', exp)
