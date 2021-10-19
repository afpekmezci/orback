import random
import string
from core.utils import SendEMail, SendSms
from django.template.loader import get_template
from organization.models import OrganizationUser
from core.settings import API_URL, CLIENT_URL


def generate_random_password(lenght):
	password = ''
	for i in range(lenght):
		password += random.choice(string.ascii_letters)
	return password


def send_register_mail(user, password):
	context = {"mail": user.email, "name": user.name, "password": password}

	plaintext = get_template("register_information_mail.txt")
	text_content = plaintext.render(context)

	htmly = get_template("register_information_mail.html")
	html_content = htmly.render(context)
	subject = "Orbone'a Hoşgeldiniz."

	print('SEND SMS CONTEXT : ', text_content)
	SendEMail().send(html_content, text_content, subject, user.email)
	if user.phone:
		SendSms().send(text_content, user.phone)

	return True

def send_forget_password_mail(forget):
	address = f"{CLIENT_URL}/kullanici/sifre-yenile/{forget.forget_code}"
	d = {
		"user": forget.user,
		"address": address,
	}
	plaintext = get_template("forget_password.txt")
	htmly = get_template("forget_password.html")
	text_content = plaintext.render(d)
	html_content = htmly.render(d)
	subject = f"Şifre Yenileme Talebi"
	SendEMail().send(html_content, text_content, subject, forget.user.email)
	if forget.user.phone:
		SendSms().send(text_content, forget.user.phone)

def serialize_user_organizations(organizations):
	data = []

	for item in organizations:
		data.append({
			'id': item.id,
			'name': item.name,
			'city': item.city
		})
	return data

def get_user_organization(user):
	organizations = OrganizationUser.objects.filter(user=user)
	data = serialize_user_organizations(organizations)
	return data
