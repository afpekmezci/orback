from django.db import models
from base.models import BaseModel
from core.settings import AUTH_USER_MODEL
from django.utils.translation import gettext as _
from organization.mails import send_invitation_mail
from base.managers import BaseManager
from files.models import BaseFileModel

class OrganizationManager(BaseManager):
	pass

class Organization(BaseModel):

	name = models.CharField(verbose_name=_('Company Name'), max_length=128)
	city = models.CharField(verbose_name=_('City'), blank=True, null=True, max_length=64)
	main_organization = models.BooleanField(default=False, verbose_name='main org')
	objects = BaseManager()

	def __str__(self):
		return f"{self.name} ({self.city if self.city is not None else ''})"

	def add_user(self, user, is_admin=False):
		"""
		Adds a new user and if the first user makes the user an admin and
		the owner.
		"""
		users_count = self.user_organizatons.all().count()
		if users_count == 0:
			is_admin = True
		# TODO get specific org user?
		org_user = OrganizationUser.objects.create(
			user=user,
			organization=self,
			is_admin=is_admin,
			is_active=True
		)
		if users_count == 0:
			# TODO get specific org user?
			OrganizationOwner.objects.create(organization=self,
												 organization_user=org_user)

		return org_user

	def remove_user(self, user):
		"""
		Deletes a user from an organization.
		"""
		org_user = self._org_user_model.objects.get(user=user,
													organization=self)
		org_user.delete()

	def get_or_add_user(self, user, **kwargs):
		"""
		Adds a new user to the organization, and if it's the first user makes
		the user an admin and the owner. Uses the `get_or_create` method to
		create or return the existing user.

		`user` should be a user instance, e.g. `auth.User`.

		Returns the same tuple as the `get_or_create` method, the
		`OrganizationUser` and a boolean value indicating whether the
		OrganizationUser was created or not.
		"""
		is_admin = kwargs.pop('is_admin', False)
		users_count = self.user_organizatons.all().count()
		if users_count == 0:
			is_admin = True

		org_user, created = OrganizationUser.objects \
			.get_or_create(organization=self,
						   user=user,
						   defaults={'is_admin': is_admin})
		if users_count == 0:
			OrganizationOwner.objects \
				.create(organization=self, organization_user=org_user)
		return org_user, created

	def change_owner(self, new_owner):
		"""
		Changes ownership of an organization.
		"""
		self.owner.organization_user = new_owner
		self.owner.save()

	def is_employee(self, user):
		return True if OrganizationUser.objects.filter(organization=self,user__in=[user]) else False

	def is_admin(self, user):
		return True if OrganizationUser.objects.filter(organization=self,user__in=[user], is_admin=True) else False

	def is_owner(self, user):
		"""
		Returns True is user is the organization's owner, otherwise false
		"""
		try:
			return self.owner.organization_user.user == user
		except:
			return False

	def save(self, *args, **kwargs):
		if not Organization.objects.filter(main_organization=True):
			self.main_organization = True
		else:
			self.main_organization= False
		super(Organization, self).save()

class OrganizationUser(BaseModel):

	user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organization_user')
	organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE, related_name='user_organizatons')
	is_admin = models.BooleanField(verbose_name='Is Admin', default=False)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['user', 'organization'], name="user-organization")
		]

	def __str__(self):
		return f"{self.organization.name} {self.user.name}"

class OrganizationOwner(BaseModel):
	organization = models.OneToOneField('organization.Organization', on_delete=models.CASCADE, related_name='owner')
	organization_user = models.OneToOneField('organization.OrganizationUser', on_delete=models.CASCADE, related_name='owner_user')

	def __str__(self):
		return f"{self.organization.name} {self.organization_user.user.name}"

class OrganizationFileManager(BaseManager):
	pass

class OrganizationFile(BaseFileModel):

	organization = models.ForeignKey(
		Organization,
		on_delete=models.CASCADE,
		verbose_name='Organization',
		related_name='organization_files'
	)

	date = models.DateTimeField(auto_now=False)
	objects = BaseManager()
	def __str__(self):
		return f"{self.title}, {self.organization}"

class OrganizationUserFile(BaseFileModel):

	organization_user = models.ForeignKey(
		OrganizationUser,
		on_delete=models.CASCADE,
		verbose_name='Organization',
		related_name='organization_user_files'
	)

	date = models.DateTimeField(auto_now=False)
	objects = BaseManager()
	def __str__(self):
		return f"{self.title}, {self.organization}"