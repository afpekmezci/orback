from django.contrib import admin

from customuser.models import User, ForgetPassword

admin.site.register(User)

@admin.register(ForgetPassword)
class ForgetPasswordAdmin(admin.ModelAdmin):
	list_display = ['user', 'forget_code', 'is_active']
	pass