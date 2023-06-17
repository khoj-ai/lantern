from django.contrib import admin
from beta_product.models import UserInterest


@admin.register(UserInterest)
class UserInterestAdmin(admin.ModelAdmin):
    user = UserInterest.user
    field = UserInterest.field
    list_display = ("user", "field", "unique_identifier", "waitlist")
    list_filter = ("user", "field")
    search_fields = ("user", "field", "unique_identifier")
    ordering = ("user", "field")
    readonly_fields = ("user", "field", "unique_identifier")
    fieldsets = (
        (None, {"fields": ("user", "field", "waitlist", "unique_identifier")}),
    )
