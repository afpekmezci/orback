from django.contrib import admin

from supplier.models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass
