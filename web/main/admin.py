from allauth.account.models import EmailAddress
from django.contrib import admin
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from main.services import UserService
from user_profile.admin import ProfileInline

User = get_user_model()


class EmailsInline(admin.TabularInline):
    """Class for inherit emails table to UserAdmin"""
    model = EmailAddress
    can_delete = False
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False if obj else True


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ('-id',)
    list_display = ('email', 'full_name', 'phone_number', 'is_active', 'email_verified')
    inlines = (EmailsInline, ProfileInline)
    list_select_related = ('profile',)
    readonly_fields = ('id',)

    def get_inlines(self, request, obj):
        return self.inlines if obj else (EmailsInline,)

    def email_verified(self, obj):
        return obj.email_address[0].verified if obj.email_address else False
    email_verified.boolean = True
    search_fields = ('first_name', 'last_name', 'email')

    fieldsets = (
        (_('Personal info'), {'fields': ('id', 'first_name', 'last_name', 'email', 'phone_number')}),
        (_('Secrets'), {'fields': ('password',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    def get_queryset(self, request):
        email_prefetch = UserService.email_address_prefetch()
        return super(CustomUserAdmin, self).get_queryset(request).prefetch_related(email_prefetch)


title = settings.MICROSERVICE_TITLE

admin.site.site_title = title
admin.site.site_header = title
admin.site.site_url = '/'
admin.site.index_title = title

admin.site.unregister(Group)
