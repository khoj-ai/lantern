from django.contrib import admin

from user_manager.models import UserMetadata

@admin.register(UserMetadata)
class UserMetadataAdmin(admin.ModelAdmin):
    user = UserMetadata.user
    guid = UserMetadata.guid
    list_display = ('user', 'guid')
    list_filter = ('user', 'guid')
    search_fields = ('user', 'guid')
    ordering = ('user', 'guid')
    readonly_fields = ('user', 'guid')
    fieldsets = (
        (None, {
            'fields': ('user', 'guid')
        }),
    )
