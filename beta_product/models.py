from django.db import models
from django.contrib.auth.models import User
from timestampedmodel import TimestampedModel

# Create your models here.
class InterestFields(models.Choices):
    ART = "Art"
    BUSINESS = "Business"
    EDUCATION = "Education"
    ENTERTAINMENT = "Entertainment"
    HEALTH = "Health"
    POLITICS = "Politics"
    SCIENCE = "Science"
    SPORTS = "Sports"
    TECHNOLOGY = "Technology"
    RESEARCH = "Research"
    OTHER = "Other"

class UserInterest(TimestampedModel):
    class Meta:
        unique_together = ['user', 'field']

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
    field = models.CharField(max_length=20, choices=InterestFields.choices, default=InterestFields.OTHER)
    waitlist = models.BooleanField(default=True)
