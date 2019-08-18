from django.contrib import admin
from .models import Ground,Reservation,Rating
from import_export.admin import ImportExportModelAdmin

@admin.register(Ground,Reservation,Rating)
class ViewAdmin(ImportExportModelAdmin):
    pass

