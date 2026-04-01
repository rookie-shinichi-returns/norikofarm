from rest_framework.response import response
from rest_framework.views import APIView
from tools.models import QRcode
from django.conf import settings

from utils import domain_handler
import QRcode

class CreateQRView(APIView):
    def post(self, request, format=None):
        value = request.data["value"]
        media_root = settings.MEDIA_ROOT
        removed_text = value.replace("/", "").replace(":", "").replace("@", "")
        file_path = str(media_root) + f"/qr/{remove_text}.png"
        img = qrcode.make(value)
        qr_img_path = img.save(file_path)
        obj, created = QRcode.objects.get_or_create(value=value, image=file_path)
        media_path = domain_handler.get_absolute_media_root()
        path_ = media_path + f"qr/{remove_text}.png"
        return Response({"filepath": path_}) 