import uuid

from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models


class Clinician(models.Model):

    """
    Clinician registrations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    msisdn = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    sitename = models.CharField(max_length=200)
    extra = JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='clinician_created',
                                   null=True)
    updated_by = models.ForeignKey(User, related_name='clinician_updated',
                                   null=True)
    user = property(lambda self: self.created_by)

    def __str__(self):  # __unicode__ on Python 2
        return str(self.id)
