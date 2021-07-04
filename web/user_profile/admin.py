from django.contrib import admin

from user_profile.models import Profile


class ProfileInline(admin.TabularInline):
    model = Profile
