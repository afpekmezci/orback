import random
import string
from core.utils import SendEMail
from django.template.loader import get_template

def send_invitation_mail(user, organization_name):
	context = {"mail": user.email, "name": user.name, "organization_name": organization_name}

	plaintext = get_template("email.txt")
	text_content = plaintext.render(context)

	htmly = get_template("invitation_mail.html")
	html_content = htmly.render(context)
	subject = f"{organization_name}'a Sizi Ekledi."

	print('SEND MAIL CONTEXT : ', context)
	SendEMail().send(html_content, text_content, subject, user.email)

	return True
