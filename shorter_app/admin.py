from django.contrib import admin
from .models import Users, Links


@admin.register(Users)
class Users(admin.ModelAdmin):
    pass


@admin.register(Links)
class Links(admin.ModelAdmin):
    pass
