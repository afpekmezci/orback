from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from note.models import Note
from note.permissions import MainPermission, RequiredFieldCheckPermission
from note.serializers import NoteSerializer


class NoteFilterBackend:
    """list note için varsayılan filter classıdır."""

    def filter_queryset(self, request, queryset, view):
        filter_kwargs = {
            "created_by_id__organization": request.org.id,
            "content_type__app_label": view.app_label
            or request.POST["app_label"],
            "content_type__model": view.model_name
            or request.POST["model_name"],
            "object_id": (
                view.kwargs[view.id_field_name]
                if view.id_field_name
                else request.POST["object_id"]
            ),
            "is_deleted": False,
        }
        return queryset.filter(**filter_kwargs)


class DataWithRequiredFieldMixin:
    app_label = None
    model_name = None
    id_field_name = None
    is_file=True
    def get_serializer(self, *args, **kwargs):
        data = kwargs["data"].copy()
        data["app_label"] = self.app_label or kwargs["data"]["app_label"]
        data["model_name"] = self.model_name or kwargs["data"]["model_name"]
        data["object_id"] = (
            self.kwargs.get(self.id_field_name)
            if self.id_field_name
            else kwargs["data"]["object_id"]
        )
        kwargs["data"] = data
        return super().get_serializer(*args, **kwargs)


class NoteCreateView(DataWithRequiredFieldMixin, CreateAPIView):
    permission_classes = [
        IsAuthenticated,
        MainPermission,
        RequiredFieldCheckPermission,
    ]
    serializer_class = NoteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["detay"] = False
        return context


class NoteUpdateViewSet(DataWithRequiredFieldMixin, UpdateAPIView):
    permission_classes = [
        IsAuthenticated,
        MainPermission,
        RequiredFieldCheckPermission,
    ]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "note_id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["detay"] = True
        return context


class NoteDeleteViewSet(DataWithRequiredFieldMixin, UpdateAPIView):
    permission_classes = [
        IsAuthenticated,
        MainPermission,
        RequiredFieldCheckPermission,
    ]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "note_id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["detay"] = True
        return context


class NoteDetailView(RetrieveAPIView):
    permission_classes = [
        IsAuthenticated,
        MainPermission,
        RequiredFieldCheckPermission,
    ]
    is_file=False
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "note_id"
    http_method_names = ["post"]

    # custom attrs
    app_label = None
    model_name = None
    id_field_name = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["detay"] = True
        return context

    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class NoteListView(ListAPIView):
    permission_classes = [
        IsAuthenticated,
        MainPermission,
        RequiredFieldCheckPermission,
    ]
    is_file=False

    filter_backends = [NoteFilterBackend]
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    http_method_names = ["post"]

    # custom attrs
    app_label = None
    model_name = None
    id_field_name = None

    def post(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
