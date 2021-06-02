from django.contrib import admin
from .models import LikeDislike


@admin.register(LikeDislike)
class LikeAdmin(admin.ModelAdmin):
    pass
