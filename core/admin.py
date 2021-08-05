from django.utils import timezone

from django.contrib import admin


# Register your models here.

@admin.action(description='Logical Delete')
def logical_delete(modeladmin, request, queryset):
    queryset.update(deleted=True, delete_time_stamp=timezone.now())


admin.site.add_action(logical_delete)
