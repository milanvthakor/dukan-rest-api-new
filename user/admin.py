from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User

# to be display in Admin console
class UserAdmin(BaseUserAdmin):
	list_display = ('email', 'name', 'phone', 'gender', 'date_joined', 'last_login', 'is_active')
	search_fields = ('email', 'name', 'phone', 'gender')
	readonly_fields = ('date_joined', 'last_login')
	ordering = ('email',)

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

	# need to define this as we don't have username
	# these are the fields that will be display to admin in add user form
	add_fieldsets = (
		(None, {
			'classes': ('wide', ),
			'fields': ('email', 'password1', 'password2'),
		}),
	)

admin.site.register(User, UserAdmin)