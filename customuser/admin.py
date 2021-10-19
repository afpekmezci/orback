from django.contrib import admin

from customuser.models import User, ForgetPassword

admin.site.register(User)

@admin.register(ForgetPassword)
class ForgetPasswordAdmin(admin.ModelAdmin):
	list_display = ['user', 'forget_code', 'is_active']
	pass

from rest_framework_simplejwt import token_blacklist

class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

	def has_delete_permission(self, *args, **kwargs):
		return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)