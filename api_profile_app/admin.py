from django.contrib import admin

from api_profile_app.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    fields = [
        'uid',
        'username',
        'avatar',
        'first_name',
        'last_name',
        'gender',
        'birthday',
        'additional_information',
        'is_active',
        'created_at',
        'updated_at',
    ]

    readonly_fields = ['username', 'uid', 'created_at', 'updated_at']

    list_display = (
        'uid', 'username', 'first_name', 'last_name',
        'gender', 'avatar', 'birthday',
        'created_at', 'updated_at', 'is_active')
    # list_editable = ('is_delete',)
    list_filter = ('gender', 'birthday', 'created_at', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')
