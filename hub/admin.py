from django.contrib import admin

from .models import FacilityCode


class FacilityCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "created_at"]
    list_filter = ["code", "created_at"]


admin.site.register(FacilityCode, FacilityCodeAdmin)
