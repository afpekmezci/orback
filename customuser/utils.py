import random
import string
from core.utils import SendEMail
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

	plaintext = get_template("email.txt")
	text_content = plaintext.render(context)

	htmly = get_template("register_information_mail.html")
	html_content = htmly.render(context)
	subject = "Orbone'a Hoşgeldiniz."

	print('SEND MAIL CONTEXT : ', context)
	SendEMail().send(html_content, text_content, subject, user.email)

	return True

def send_forget_password_mail(forget):
	address = f"{CLIENT_URL}/kullanici/forgetpassword/{forget.forget_code}"
	d = {
		"user": forget.user,
		"address": address,
	}
	plaintext = get_template("email.txt")
	htmly = get_template("forget_password.html")
	text_content = plaintext.render(d)
	html_content = htmly.render(d)
	subject = f"Şifre Yenileme Talebi"
	SendEMail().send(html_content, text_content, subject, forget.user.email)

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
	print('USER : ', user)
	organizations = OrganizationUser.objects.filter(user=user)
	print('ORGANİZATİONS : ', organizations)
	data = serialize_user_organizations(organizations)
	return data
