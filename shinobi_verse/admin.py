from django.contrib import admin

from shinobi_verse.models import Shinobi, Clan, Jutsu
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
# registration your models here.


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('User Roles', {'fields': ('groups',)}),
    )


@admin.register(Shinobi)
class ShinobiAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'village', 'created_at')
    list_filter = ('village', 'rank', 'clan')
    search_fields = ('name', 'bio', 'village')
    ordering = ('-created_at',)
    list_editable = ('rank',)


@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    list_display = ('name', 'founder', 'village')
    list_filter = ('approved',)
    search_fields = ('name', 'description')
    ordering = ('-id',)


@admin.register(Jutsu)
class JutsuAdmin(admin.ModelAdmin):
    list_display = ('name', 'chakra_type', 'jutsu_type', 'description')
    list_filter = ('jutsu_type', 'approved')
    search_fields = ('name', 'description')

