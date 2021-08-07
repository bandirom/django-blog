from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from .models import LikeDislike, Follower, Action


@admin.register(LikeDislike)
class LikeAdmin(admin.ModelAdmin):
    list_select_related = ('user', 'content_type')
    list_display = ('user', 'content_type', 'vote', 'date', 'content_object')
    list_filter = ('vote',)


class LikeDislikeInline(GenericTabularInline):
    model = LikeDislike
    extra = 0


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'to_user', 'created')
    date_hierarchy = 'created'


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'date')
