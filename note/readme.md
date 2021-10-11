Usage;

Öncelikle bu modulün extand edileceği modulün url'lerine aşağıdaki gibi bir url bloğu ekleriz.

```python
from note.viewsets import (
    ListView as NoteListView,
    CreateView as NoteCreateView,
    UpdateView as NoteUpdateView,
    DetailView as NoteDetailView,
)
from {app_name}.permissions import CustomPermission

# Hepsi Post Metodu olarak çalışır.

urlpatterns = [
    path("<int:{id_field_name}>/notes/", NoteListView.as_view(
            app_label="{app_name}",
            model_name="{model_name}",
            id_field_name="{id_field_name}",
            permission_classes=NoteListView.permission_classes + [CustomPermission],
            filter_backends=NoteListView.filter_backends + [],
        ),
        name="{app_name}_note_list",
    ),
    path("<int:{id_field_name}>/note/create/", NoteCreateView.as_view(
            app_label="{app_name}",
            model_name="{model_name}",
            id_field_name="{id_field_name}",
            permission_classes=NoteCreateView.permission_classes + [CustomPermission],
            filter_backends=NoteCreateView.filter_backends + [],
        ),
        name="{app_name}_note_create",
    ),
    path("<int:{id_field_name}>/note/update/<int:note_id>/", NoteUpdateView.as_view(
            app_label="{app_name}",
            model_name="{model_name}",
            id_field_name="{id_field_name}",
            permission_classes=NoteUpdateView.permission_classes + [CustomPermission],
            filter_backends=NoteUpdateView.filter_backends + [],
        ),
        name="{app_name}_note_update",
    ),
    path("<int:{id_field_name}>/note/detail/<int:note_id>/", NoteDetailView.as_view(
            app_label="{app_name}",
            model_name="{model_name}",
            id_field_name="{id_field_name}",
            permission_classes=NoteDetailView.permission_classes + [CustomPermission],
            filter_backends=NoteDetailView.filter_backends + [],
        ),
        name="{app_name}_note_detail",
    ),
]
```

Eğer Module özel permission sınıfı gerekirse, modulün altında permission.py diye bir dosya açarak,

permission class'ını import edip, kendi custom permission'i yazılabilir,


```python
from rest_framework import permissions


from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)


class CustomPermission(permissions.BasePermission):
    "Benim custom permission class'ım"
    
    def has_permission(self, request, view):
        "sadece ListAPIView class'ı kullanılarak yazılan viewlerde çalışır"
        return True

    def has_object_permission(self, request, view, obj):
        "buradaki obj note'dur"
        "CreateAPIView, RetrieveAPIView, UpdateAPIView class'ı kullanılarak yazılan viewlerde çalışır"
        return True


# eğer note değilde, nota bağlı model bazlı permission kontrol yapılmak isteniyor ise

from note.permissions import BaseContentObjectPermission
# bu class miras alınarak yazılan her permission CreateAPIView,
#     ListAPIView,
#     RetrieveAPIView,
#     UpdateAPIView,
# ) viewllerinde çalışır.

class CustomContentObjectPermission(BaseContentObjectPermission):
    """NOTE; bu permission class'ı note instance yerine content object de
    permission belirlemek içindir.

    USAGE;

    class CustomNotePermission(BaseNotePermission):

        def has_object_permission(self, request, view, obj):
            return True
    """


```

permission yazıltıktan sonra urls.py dosyasına ilgili permission class'ı yazılmalıdır.
`permission_classes=NoteListView.permission_classes + [CustomContentObjectPermission],`
gibi


dönen not querysetlerine extra filter uygulanmak isteniyor ise, filters.py adında bir dosya açılmalı, ve aşağıdakine benzer bir class yazılmalıdır.

```python

from note.models import Note

class CustomFilterBackend:

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user__username="hakan")

```

bu filterin uygulanması istenilen url'ye `filter_backends=NoteCreateView.filter_backends + [CustomFilterBackend],` şeklinde yazılmalı.
