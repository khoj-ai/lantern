from django.contrib import admin
from beta_product.models import UserInterest
from import_export.admin import ExportActionMixin

from import_export import resources
from beta_product.models import UserInterest


class UserInterestResource(resources.ModelResource):
    class Meta:
        model = UserInterest
        fields = ("id", "user__email")


class UserInterestExportActionMixin(ExportActionMixin):
    def get_export_resource_class(self):
        """
        Returns the ResourceClass to use for this view.
        """
        return UserInterestResource


class UserInterestAdmin(UserInterestExportActionMixin, admin.ModelAdmin):
    user = UserInterest.user
    field = UserInterest.field
    list_display = ("user", "field", "unique_identifier", "waitlist")
    list_filter = ("user", "field")
    search_fields = ("user", "field", "unique_identifier")
    ordering = ("user", "field")
    fieldsets = (
        (None, {"fields": ("user", "field", "waitlist", "unique_identifier")}),
    )


admin.site.register(UserInterest, UserInterestAdmin)
