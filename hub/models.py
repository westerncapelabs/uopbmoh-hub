# Models go here
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class FacilityCode(models.Model):
    """
    This is a list of all acceptable facility codes in the system
    """
    code = models.CharField(null=False, max_length=100, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)
