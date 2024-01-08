"""Django admin customization"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models
from scrapping.models import Informations, Pages
from django.forms import FileInput


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important date'), {'fields': ('last_login',)}
        ),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


admin.site.register(models.User, UserAdmin)


@admin.register(Informations)
class MangaInformations(admin.ModelAdmin):
    list_display = (
        'author',
        'release_date',
        'category',
    )


@admin.register(Pages)
class MangaPages(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'number_chapter',)
    list_per_page = 10
    list_filter = ('informations',)
