import random
import string
from core.utils import SendEMail, SendSms
from django.template.loader import get_template

def send_invitation_mail(organization_user):
	context = {"mail": organization_user.user.email, "name": organization_user.user.name, "organization_name": organization_user.organization.name}

	plaintext = get_template("invitation_mail.txt")
	text_content = plaintext.render(context)

	htmly = get_template("invitation_mail.html")
	html_content = htmly.render(context)
	subject = f"{organization_user.organization.name}'a Sizi Orbone'a Ekledi."

	print('SEND MAIL CONTEXT : ', context)
	SendEMail().send(html_content, text_content, subject, organization_user.user.email)
	if organization_user.user.phone:
		SendSms().send(text_content, organization_user.user.phone)
	return True
