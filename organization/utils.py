
from organization.models import Organization

def get_main_org():
	try:
		return Organization.objects.get(main_organization=True)
	except Organization.DoesNotExist:
		return None