

def can_edit(obj, request):
	if request.org.main_organization:
		return True
	if obj.created_by == request.user or request.org.is_owner(request.user):
		return True

	return False