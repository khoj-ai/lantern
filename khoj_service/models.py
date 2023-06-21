from django.db import models
from django.contrib.auth.models import User
from khoj_service.managers import RoutingTableQuerySet


class RoutingTable(models.Model):
    objects = RoutingTableQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
