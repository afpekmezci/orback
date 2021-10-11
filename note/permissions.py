from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions
from note.models import Note


def get_app_label(request, view):
    """as_view ile verilen veya POST içindeki data da app_label'i alır."""
    return (
        view.app_label
        if hasattr(view, "app_label") and view.app_label
        else request.POST.get("app_label")
    )


def get_model_name(request, view):
    """as_view ile verilen veya POST içindeki data da model_name'i alır."""
    return (
        view.model_name
        if hasattr(view, "model_name") and view.model_name
        else request.POST.get("model_name")
    )


def get_object_id(request, view):
    """as_view ile verilen veya POST içindeki data da object_id'i alır."""
    return (
        view.kwargs[view.id_field_name]
        if hasattr(view, "id_field_name") and view.id_field_name
        else request.POST.get("object_id")
    )


class MainPermission(permissions.BasePermission):
    """genel permission'ı kontrol eder, her istekte çalışır."""

    def has_permission(self, request, view):
        """

        try:
            get_organization_details(request, Note)
        except Exception as e:
            self.message = e
            return False
        else:
            return True
        """
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class RequiredFieldCheckPermission(permissions.BasePermission):
    """App label and Model name check in Body."""

    def has_permission(self, request, view):
        app_label = get_app_label(request, view)
        model_name = get_model_name(request, view)
        object_id = get_object_id(request, view)
        if not all((app_label, model_name, object_id)):
            self.message = (
                "Body should contain app_label, model_name, object_id"
            )
            return False
        content_type = ContentType.objects.get(
            model=model_name, app_label=app_label
        )
        try:
            content_type.get_object_for_this_type(id=object_id)
        except content_type.model_class().DoesNotExist:
            self.message = "There is no such object."
            return False
        else:
            return True


class BaseContentObjectPermission(permissions.BasePermission):
    """NOTE; bu permission class'ı note instance yerine content object de
    permission belirlemek içindir.

    USAGE;

    class CustomNotePermission(BaseNotePermission):

        def has_object_permission(self, request, view, obj):
            return True
    """

    def has_permission(self, request, view):
        obj = Note.get_content_object(
            app_label=get_app_label(request, view),
            model_name=get_model_name(request, view),
            object_id=get_object_id(request, view),
        )
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        if isinstance(obj.__class, Note):
            return super().has_object_permission(
                request, view, obj.get_object()
            )
        else:
            return super().has_object_permission(request, view, obj)

class OrganizationEqualPermission(BaseContentObjectPermission):
    message = "Permission Denied"

    def has_object_permission(self, request, view, obj):
        return obj.created_by_id.organization.id == request.org.id
