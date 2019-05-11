from django.contrib import admin
from .models import ExtendUser, Activity
from .forms import ExtendUserAdminForm, ActivityAdminForm

# Register your models here.

class ExtendUserAdmin(admin.ModelAdmin):
    form = ExtendUserAdminForm
    search_fields = ('studentId',)

class ActivityAdmin(admin.ModelAdmin):
    form = ActivityAdminForm
    list_display = ('id', 'title')
    search_fields = ('title',)

admin.site.register(ExtendUser, ExtendUserAdmin)
admin.site.register(Activity, ActivityAdmin)
