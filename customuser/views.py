from django.shortcuts import render
from uuid import uuid4
from customuser.models import User, ForgetPassword
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenViewBase
)
from customuser.serializers import (
	TokenObtainPairPatchedSerializer,
	TokenRefreshPatchedSerializer,
	TokenRefreshPatchedSerializerForWeb,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from customuser.serializers import UserSerializer, ForgetSerializer, ResetPasswordSerializer
from django.shortcuts import get_object_or_404
from core.settings import API_URL, CLIENT_URL
from customuser.utils import send_forget_password_mail
from base.views import PatchAPIView

class UserDetailView(generics.RetrieveAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    def get_object(self):
      queryset = self.queryset.filter(pk=self.request.user.pk)
      obj = get_object_or_404(queryset)
      return obj


class ForgetPasswordView(APIView):

    permission_classes = [permissions.AllowAny]  # Or anon users can't register
    serializer_class = ForgetSerializer
    def post(self, request):
        if not request.data.get('email'):
            return Response(
                "Email Required", status=status.HTTP_400_BAD_REQUEST
            )
        try:
            _user = User.objects.get(email__exact=request.data.get('email'))
        except User.DoesNotExist:
            return Response("Wrong Email", status=status.HTTP_400_BAD_REQUEST)
        try:
            # önceki forget password isteklerini deactive eder.
            _olds = ForgetPassword.objects.filter(
                user__email__exact=request.data.get('email')
            ).all()
            for old in _olds:
                old.is_active = False
                old.save()
        except ForgetPassword.DoesNotExist:
            pass
        forget = ForgetPassword()
        forget.forget_code = uuid4()
        forget.user = _user
        forget.save()
        send_forget_password_mail(forget)
        return Response("Email Sended", status=status.HTTP_200_OK)


class ResetPasswordView(generics.UpdateAPIView):
    model = ForgetPassword
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer
    queryset = ForgetPassword.objects.all()
    lookup_field = 'forget_code'

    def get_object(self):
      queryset = self.queryset.filter(forget_code=self.request.data.get(self.lookup_field))
      obj = get_object_or_404(queryset)
      return obj


class ChangePasswordView(PatchAPIView):
    model=User
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get_object(self):
        queryset = self.queryset.filter(pk=self.request.user.pk)
        obj = get_object_or_404(queryset)
        return obj

class TokenObtainPairPatchedView(TokenViewBase):
    serializer_class = TokenObtainPairPatchedSerializer

class TokenRefreshPatchedView(TokenRefreshView):
    serializer_class = TokenRefreshPatchedSerializer
    token_refresh = TokenRefreshView.as_view()


class TokenRefreshPatchedViewForWeb(TokenRefreshView):
    serializer_class = TokenRefreshPatchedSerializerForWeb
    token_refresh = TokenRefreshView.as_view()