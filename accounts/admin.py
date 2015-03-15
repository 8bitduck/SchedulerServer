from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import User
from api.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

class CustomUserAdmin(UserAdmin):

	fieldset = (
		(None, {'fields': ('email', 'password')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2')}
		),
	)

	form = CustomUserChangeForm
	add_form = CustomUserCreationForm
	list_display = ('email', 'mobile_number', 'first_name', 'last_name', 'is_active', 'is_admin', 'is_staff',)
	search_fields = ('mobile_number', 'first_name', 'last_name',)
	ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)