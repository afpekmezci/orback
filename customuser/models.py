from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from core.utils import get_upload_path
from customuser.utils import generate_random_password, send_register_mail
from base.models import BaseModel

class UserManager(BaseUserManager):
	def create_user(self, email, name, phone=None):

		if not email:
			raise ValueError("E-Posta adresi girilmesi zorunludur")

		email = email.lower()

		user = self.model(email=self.normalize_email(email), name=name, phone=phone, is_active=True)

		password = generate_random_password(8)
		user.set_password(password)
		user.save(using=self._db)
		send_register_mail(user, password)
		return user

	def update_user(self, email, password):
		pass

	def create_superuser(self, email, name, password):

		user = self.create_user(
			email=self.normalize_email(email),
			name=name,
		)
		user.is_staff = True
		user.is_superuser = True
		user.is_active = True
		user.save(using=self._db)

		user.set_password(password)
		return User


class User(AbstractUser):

	username = None
	first_name = None
	last_name = None

	email = models.EmailField(
		verbose_name="Email", max_length=120, unique=True
	)

	is_active = models.BooleanField(default=False)

	invited_by = models.ForeignKey('self',
		verbose_name="Davet Eden",
		on_delete=models.PROTECT,
		related_name="user_invited_by",
		blank=True,
		null=True,
	)

	name = models.CharField(verbose_name='İsim', max_length=64)
	phone = models.CharField(verbose_name='Phone', max_length=13, unique=True, null=True, blank=True)
	is_first = models.BooleanField(verbose_name='is first', default=True)

	person_image = models.ImageField(
		upload_to=get_upload_path, blank=True, null=True
	)

	person_thumbnail = models.ImageField(
		upload_to=get_upload_path, blank=True, null=True
	)

	is_public = models.BooleanField(
		verbose_name="Başkaları tarafından görüntülenebilir mi?", default=False
	)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ['name']
	objects = UserManager()

	def __str__(self):
		return f"{self.email} {self.name}"

	def has_module_perms(self, app_label):
		return True


class ForgetPassword(BaseModel):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forget_password')
	forget_code = models.CharField(verbose_name="Davet kodu", max_length=128)
	is_active = models.BooleanField(verbose_name="Is Active", default=True)
