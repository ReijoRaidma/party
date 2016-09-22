from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from parties.models import Party, Guest, User

admin.site.register(Party)
admin.site.register(Guest)

admin.site.register(User, UserAdmin)
