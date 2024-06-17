from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User









class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password','first_name', 'last_name','last_login', )}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2','first_name', 'last_name')
            }
        ),
    )

    list_display = ('email', 'id','first_name','last_name', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    list_display_links = ('email','first_name','last_name','id',)
    search_fields = ('email',)
    ordering = ["-date_joined", 'id'] 
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)
