from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Developer, Client, WorkExperience, Skill, Education


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'first_name', 'last_name', 'is_active', 'is_developer', 'is_client',)
    list_filter = ('email', 'is_staff', 'first_name', 'last_name', 'is_active','is_developer', 'is_client', )
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active' , 'is_developer', 'is_client')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active', 'is_developer', 'is_client')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email', 'first_name', 'last_name',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Developer)
admin.site.register(Client)
admin.site.register(WorkExperience)
admin.site.register(Skill)
admin.site.register(Education)
