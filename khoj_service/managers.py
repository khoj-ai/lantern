from django.db import models


class RoutingTableQuerySet(models.QuerySet):
    def get_by_user(self, user):
        return self.filter(user=user)

    def get_service_url_by_user(self, user):
        user = self.get_by_user(user)
        if user.exists():
            return user.first().url
        return None
