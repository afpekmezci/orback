from rest_framework import serializers
from organization.models import Organization, OrganizationUser, OrganizationOwner, OrganizationFile
from customuser.models import User
from core.get_request import current_request
from rest_framework.exceptions import PermissionDenied
from files.serializers import BaseFileSerializer
from base.fields import TimestampField


class OrganizationSerializer(serializers.ModelSerializer):
	owner_name = serializers.CharField(required=True, write_only=True)
	owner_mail = serializers.CharField(required=True, write_only=True)
	is_owner = serializers.SerializerMethodField()
	role = serializers.SerializerMethodField()

	def to_representation(self, instance):
		data = super(OrganizationSerializer, self).to_representation(instance)
		try:
			owner = OrganizationOwner.objects.get(organization=instance)
			data['owner_name'] = owner.organization_user.user.name
			data['owner_mail'] = owner.organization_user.user.email
		except:
			pass
		return data
	@staticmethod
	def get_is_owner(obj):
		req = current_request()
		return obj.is_owner(req.user)

	@staticmethod
	def get_role(obj):
		role = 'guest'
		request = current_request()
		if obj.main_organization:
			role = 'main'
		elif obj.is_owner(request.user):
			role = 'organization_owner'
		else:
			role = 'personel'
		return role
	def create(self, validated_data):
		user_name = validated_data.pop('owner_name')
		user_email = validated_data.pop('owner_mail')
		instance = super(OrganizationSerializer, self).create(validated_data)

		try:
			user = User.objects.get(email=user_email)
		except:
			user = User.objects.create_user(name=user_name, email=user_email)

		instance.add_user(user, is_admin=True)
		return instance
	def update(self, instance, validated_data):

		return super(OrganizationSerializer, self).update(instance, validated_data)

	class Meta:
		model = Organization
		fields = [
			'id',
			'name',
			'city',
			'owner_name',
			'owner_mail',
			'main_organization',
			'is_owner',
			'role',
		]
		read_only_fields = ['main_organization', 'role']

class OrganizationUserSerializer(serializers.ModelSerializer):
	user_name = serializers.CharField(required=False, source='User.name', write_only=True)
	user_email = serializers.CharField(required=False, source='User.email', write_only=True)
	user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False, write_only=True)
	is_owner = serializers.SerializerMethodField()

	@staticmethod
	def get_is_owner(obj):
		return obj.organization.is_owner(obj.user)

	def to_representation(self, instance):
		data = super(OrganizationUserSerializer, self).to_representation(instance)

		data['user_name'] = instance.user.name
		data['user_email'] = instance.user.email
		data['organization'] = OrganizationSerializer(instance.organization).data
		return data
	def to_internal_value(self, data):
		data = super(OrganizationUserSerializer, self).to_internal_value(data)
		print('DATA : ', data)
		return data
	def create(self, validated_data):
		if validated_data.get('User'):
			valid_user = validated_data.pop('User')
			user_name = valid_user.pop('name')
			user_email = valid_user.pop('email')

			try:
				user = User.objects.get(email=user_email)
			except:
				user = User.objects.create_user(name=user_name, email=user_email)

		elif validated_data.get('user'):
			user = validated_data.pop('user')
		else:
			raise serializers.ValidationError('user is required')
		instance, created = validated_data.get('organization').get_or_add_user(user, is_admin=False)
		if not created:
			instance.is_active = True
			instance.save()
		return instance

	def update(self, instance, validated_data):
		return super(OrganizationUserSerializer, self).update(instance, validated_data)

	class Meta:
		model = OrganizationUser
		fields = ['id', 'user', 'organization', 'user_name', 'user_email', 'is_owner']



class OrganizationFileSerializer(BaseFileSerializer):
	date = TimestampField()
	class Meta:
		model = OrganizationFile
		fields = BaseFileSerializer.Meta.fields + ['organization', 'date']