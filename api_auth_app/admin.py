from django.contrib import admin

from api_auth_app.models import UserCodeVerify

@admin.register(UserCodeVerify)
class UserCodeVerifyAdmin(admin.ModelAdmin):

    fields = [
        'address', 'code', 'created_at', 'access_at', 'attempts_cnt'
    ]

    readonly_fields = [
        'address', 'created_at', 'access_at', 'code'
    ]

    list_display = ['address', 'attempts_cnt']
    search_fields = ['address']

