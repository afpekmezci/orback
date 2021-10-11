from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import base64
import mimetypes
from uuid import uuid4

def get_upload_path(instance, path):
	app_name = instance._meta.app_label
	# apas_id=instance.get_full_name
	path = "images/" + app_name + path
	konum = path.split("-")[0]
	"""if not os.path.exists(konum):
		os.makedirs(os.path.join(konum))"""
	return path


class SendEMail:
	def send(self, html_content, text_content, subject, to):
		subject, from_email, to = subject, settings.EMAIL_HOST_USER, to
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		status = msg.send()
		print("MAIL STATUS : ", status)


class ImageUtils:
	"""Bu class görselleri kaydetmek için base64 dataları okuyarak kendi
	formatında dosyalara çevirip anlık tarih saat bilgisine göre dosya adı
	oluşturan ve modeldeki path bilgisine göre kaydedilmek üzere fonksiyonun
	çağrıldığı serializera gönderir."""

	def CreateBase64ToImagefile(self, file_, org):
		"""bu fonksiyon orjinal görseli oluşturur."""

		__, file_data = file_.split(";base64,")
		extension = mimetypes.guess_extension(mimetypes.guess_type(file_)[0])
		print("extension", extension)
		path = "/original/%s/-" % org + str(uuid4()) + extension
		data = ContentFile(
			base64.b64decode(file_data), name=path
		)  # NOTE buraya path mı yoksa
		data.format = extension  # sanırım gereksiz
		return path, data

	def CreateBase64ToThumbnailfile(self, image, org, is_file=False):
		"""bu fonksiyon orjinal önce orjinal datayı oluşturur sonra
		boyutlandırıp png formatına çevirerek kaydedilmek üzere serializera
		gönderir."""

		if not is_file:
			filename, image = self.CreateBase64ToImagefile(image, org)

		image = Image.open(image)
		image = image.convert("RGB")
		w_percent = 200 / float(image.size[0])
		h_size = int(float(image.size[1]) * float(w_percent))
		image = image.resize((200, h_size), Image.NEAREST)
		image_io = io.BytesIO()
		image.save(
			image_io,
			dpi=(50, 50),
			optimize=True,
			quality=60,
			compress_level=7,
			format="jpeg",
		)
		path = "/thumb/%s/-" % org + "%s.jpg" % str(uuid4())
		thumb = ContentFile(image_io.getvalue(), name=path)
		return path, thumb

	def GetImageFileToBase64(self, image):
		"""bu fonksiyon modelden alınan path bilgisine göre dosyayı okuyup
		base64 olarak çağırıldığı serializera gönderir."""
		if image and image.name:
			try:
				mime_type = image.file.mime_type
			except AttributeError:
				mime_type = None
			if mime_type is None:
				extention = image.name.split(".")[-1]
				if extention is not None:
					mime_type = mimetypes.types_map[f".{extention}"]
				else:
					mime_type = ""
			img_to_base64 = base64.b64encode(image.read()).decode("utf-8")
			return f"data:{mime_type};base64,{img_to_base64}"

