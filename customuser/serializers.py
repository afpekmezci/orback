from rest_framework import serializers
from customuser.models import User, ForgetPassword
from rest_framework_simplejwt.serializers import (
	TokenObtainPairSerializer,
	TokenRefreshSerializer,
)
from organization.serializers import OrganizationSerializer
from customuser.utils import get_user_organization
from organization.models import Organization
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

def get_organization_list(user):
	organizations = Organization.objects.filter(user_organizatons__user=user)
	serialized = OrganizationSerializer(organizations, many=True)
	return {'organizations': serialized.data}


class PasswordField(serializers.CharField):
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('style', {})

		kwargs['style']['input_type'] = 'password'
		kwargs['write_only'] = True
		kwargs['required'] = True
		kwargs['min_length'] = 8
		kwargs['max_length'] = 24

		super().__init__(*args, **kwargs)

class UserSerializer(serializers.ModelSerializer):
	password = PasswordField()

	password_change = False
	@classmethod
	def get_token(cls, user):
		return RefreshToken.for_user(user)

	def to_representation(self, instance):
		data = super(UserSerializer, self).to_representation(instance)

		organizations = get_organization_list(instance)

		if self.password_change:
			refresh = self.get_token(instance)
			data['token'] = {
				'refresh': str(refresh),
				'access': str(refresh.access_token),
			}

		return {**data, **organizations}

	def update(self, instance, validated_data):

		if validated_data.get('password'):
			instance.is_first=False
			_pass = validated_data.pop('password')
			instance.set_password(_pass)
			self.password_change = True
		return super(UserSerializer, self).update(instance, validated_data)

	class Meta:
		model = User
		fields = ['id', 'name', 'email', 'is_first', 'password']
		read_only_fields = ['is_first']


class ForgetSerializer(serializers.Serializer):
	email = serializers.EmailField(required=True, write_only=True)
	class Meta:
		fields = ['email']

class ResetPasswordSerializer(serializers.Serializer):
	password = PasswordField()
	forget_code = serializers.CharField(required=True)

	def validate(self, attrs):
		instance = getattr(self, 'instance', None)

		if not instance or not instance.is_active:
			raise serializers.ValidationError('invalid forget_code')

		return attrs

	def update(self, instance, validated_data):

		instance.user.set_password(validated_data.get('password'))
		instance.user.name = 'changed name'
		print('USER : ', instance.user)
		instance.user.save()
		instance.is_active = False

		instance.save()

		return instance


class TokenObtainPairPatchedSerializer(TokenObtainPairSerializer):

	def validate(self, attrs):
		try:
			user = User.objects.get(email__exact=attrs.get("email"))
			if user.is_active is False:
				raise _user_is_inactive

		except User.DoesNotExist:
			raise serializers.ValidationError(
				{
					"detail": "No active account found with the given credentials"
				}
			)

		data = super().validate(attrs)
		user_data = UserSerializer(user)
		tokens = {'token':{"access_token": data.get('access'), "refresh_token": data.get('refresh')}}

		data = {**user_data.data, **tokens}
		return data


class TokenRefreshPatchedSerializer(TokenRefreshSerializer):
	def validate(self, attrs):
		data = super().validate(attrs)
		return {"access_token": data["access"]}


class TokenRefreshPatchedSerializerForWeb(TokenRefreshSerializer):
	refresh = serializers.CharField(required=False)
	token = serializers.JSONField(required=False)

	def validate(self, attrs):
		print('attrs : ',attrs)
		refresh = {"refresh": attrs["token"]["refresh_token"]}
		data = super().validate(refresh)
		_access_token = data["access"]

		token = {
			"access_token": _access_token,
			"refresh_token": refresh["refresh"],
		}
		return {"token": token}


