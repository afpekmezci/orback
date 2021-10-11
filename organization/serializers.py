from rest_framework import serializers
from organization.models import Organization, OrganizationUser, OrganizationOwner
from customuser.models import User

class OrganizationSerializer(serializers.ModelSerializer):
	user_name = serializers.CharField(required=True, write_only=True)
	user_email = serializers.CharField(required=True, write_only=True)


	def create(self, validated_data):
		user_name = validated_data.pop('user_name')
		user_email = validated_data.pop('user_email')
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
		fields = ['id', 'name', 'city', 'user_name', 'user_email']


class OrganizationUserSerializer(serializers.ModelSerializer):
	user_name = serializers.CharField(required=False, source='User.name', write_only=True)
	user_email = serializers.CharField(required=False, source='User.email', write_only=True)
	user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False, write_only=True)

	def to_representation(self, instance):
		data = super(OrganizationUserSerializer, self).to_representation(instance)

		data['user_name'] = instance.user.name
		data['user_email'] = instance.user.email
		data['organization'] = OrganizationSerializer(instance.organization).data
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
		fields = ['id', 'user', 'organization', 'user_name', 'user_email']