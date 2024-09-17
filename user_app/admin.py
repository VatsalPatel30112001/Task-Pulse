from django.contrib import admin
from .models import *
# Register your models here.

class RoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

admin.site.register(Role, RoleAdmin)