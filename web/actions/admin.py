from django.contrib.contenttypes import admin as cadmin
from django.contrib import admin
from .models import LikeDislike


@admin.register(LikeDislike)
class LikeAdmin(admin.ModelAdmin):
    pass


class LikeDislikeInline(cadmin.GenericTabularInline):
    model = LikeDislike
    extra = 0
