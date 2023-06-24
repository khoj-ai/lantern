from django.contrib import admin
from khoj_service.models import RoutingTable


@admin.register(RoutingTable)
class RoutingTableAdmin(admin.ModelAdmin):
    user = RoutingTable.user
    url = RoutingTable.url
    list_display = ("user", "url")
    list_filter = ("user", "url")
    search_fields = ("user", "url")
    ordering = ("user", "url")
    fieldsets = ((None, {"fields": ("user", "url")}),)
