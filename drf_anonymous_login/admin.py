from django.contrib import admin

from .models import AnonymousLogin


@admin.register(AnonymousLogin)
class AnonymousLoginAdmin(admin.ModelAdmin):
    list_display = ("token", "created")
    readonly_fields = ("token", "created", "request_data")
