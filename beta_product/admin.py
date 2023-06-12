from django.contrib import admin
from beta_product.models import UserInterest

@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    user = UserInterest.user
    field = UserInterest.field
    list_display = ('user', 'field')
    list_filter = ('user', 'field')
    search_fields = ('user', 'field')
    ordering = ('user', 'field')
    readonly_fields = ('user', 'field')
    fieldsets = (
        (None, {
            'fields': ('user', 'field')
        }),
    )
