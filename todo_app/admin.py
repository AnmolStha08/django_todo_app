from django.contrib import admin
from .models import User, Todo


admin.site.register(Todo)
# @admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')  # Include other fields as necessary 'password', 'confirmpassword'
