from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.crypto import pbkdf2
from django.conf import settings
import base64
import hashlib
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):

	def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
		if not email:
			raise ValueError('Users must have an email address')

		now = timezone.now()

		user = self.model(
			email = self.normalize_email(email),
			is_staff=is_staff,
			is_active=True,
			is_superuser=is_superuser,
			last_login=now,
			date_joined=now,
			**extra_fields
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		return self._create_user(email, password, False, False, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		return self._create_user(email, password, True, True, **extra_fields)

	def get_by_natural_key(self, email):
		if email is None:
			email=''
		return self.get(email=self.normalize_email(email))

	# def normalize_email(self, email):
	# 	salt_bytes = base64.b64decode(settings.EMAIL_SALT)
	# 	hash_bytes = pbkdf2(email.lower().strip(), salt_bytes, 1000, digest=hashlib.sha1)
	# 	email = base64.b64encode(hash_bytes).decode('ascii').strip()
	# 	return email


class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email address'), max_length=64, unique=True, db_index=True)
	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	mobile_number = models.CharField(max_length=15, null=True, blank=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'

	objects = UserManager()

	def __str__(self):
		return self.get_short_name() or str(self.id)

	def get_short_name(self):
		return self.email

	def get_full_name(self):
		return self.email	