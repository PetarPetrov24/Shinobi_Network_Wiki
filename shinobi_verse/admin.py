from django.contrib import admin

from shinobi_verse.models import Shinobi, Clan, Jutsu
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser
# registration your models here.

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_superuser', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'is_staff')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )



@admin.register(Shinobi)
class ShinobiAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'village', 'created_at', 'approved')
    list_filter = ('village', 'rank', 'clan', 'approved')
    search_fields = ('name', 'bio', 'village')
    ordering = ('-created_at',)
    list_editable = ('rank', 'approved')

    def approve_selected(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} shinobi successfully approved.")
    approve_selected.short_description = "Approve selected shinobi"

@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    list_display = ('name', 'founder', 'village', 'approved')
    list_filter = ('approved',)
    search_fields = ('name', 'description')
    ordering = ('-id',)
    list_editable = ('approved',)

    def approve_selected(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} clans successfully approved.")
    approve_selected.short_description = "Approve selected clans"

@admin.register(Jutsu)
class JutsuAdmin(admin.ModelAdmin):
    list_display = ('name', 'chakra_type', 'jutsu_type', 'description', 'approved')
    list_filter = ('jutsu_type', 'approved')
    search_fields = ('name', 'description')
    list_editable = ('approved',)

    def approve_selected(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} jutsu successfully approved.")
    approve_selected.short_description = "Approve selected jutsu"
