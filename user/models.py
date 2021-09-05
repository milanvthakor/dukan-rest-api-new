from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError("Email address is required.")
		
		user = self.model(
				email = self.normalize_email(email),
				**extra_fields
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password, **extra_fields):
		# initially save user with no permission of the super user by calling above create_user method
		# as this is a super user, here others fields are not mention
		user = self.create_user(
				email = self.normalize_email(email),
				password = password,
				**extra_fields
			)
		# provide superuser privilege to the user
		user.is_superuser = True
		user.is_staff = True
		user.save(using=self._db)
		return user

	# for case insensitive authentication
	def get_by_natural_key(self, username):
		case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
		return self.get(**{case_insensitive_username_field: username})


class User(AbstractBaseUser):
	# blank defined for admin and null for the database
	email					= models.EmailField(unique=True)
	name 					= models.CharField(max_length=150, blank=True, null=True)
	date_of_birth			= models.DateField(null=True, blank=True)
	# phone number regex for india
	phone_regex				= RegexValidator(regex=r'^(\+91)\d{10}', message="Phone number must have format of +91999999999.")
	phone 					= models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=True, null=True)
	# Gender Choices
	gender_choices = (
		('Male', 'Male'),
		('Female', 'Female'),
		('Other', 'Other')
	)
	gender 					= models.CharField(max_length=10, choices=gender_choices, null=True)
	city					= models.CharField(max_length=100, blank=True, null=True)
	# below fields are must be defined as it require by AbstractBaseTrue
	date_joined				= models.DateTimeField(auto_now_add=True)
	last_login				= models.DateTimeField(auto_now=True)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = []

	objects = UserManager()
	
	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_superuser

	def has_module_perms(self, app_labels):
		return True

# To generate the Token for new users once they successfully get stored in Database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance) 