from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "phone", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name", "phone")
    list_filter = ("is_active", "is_staff", "is_superuser")

admin.site.register(User, UserAdmin)
