from django.utils import timezone

from django.contrib import admin

from core.models import User
# Register your models here.

@admin.action(description='Logical Delete')
def logical_delete(modeladmin, request, queryset):
    queryset.update(deleted=True, delete_time_stamp=timezone.now())


admin.site.add_action(logical_delete)
admin.site.register(User)