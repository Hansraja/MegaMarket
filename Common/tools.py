import cloudinary.uploader
from Common.models import Image
from Common.types import ImageInput
from cloudinary import CloudinaryImage
import cloudinary
from django.db import router


class ImageHandler():
    def __init__(self, image_input: ImageInput = None):
        self.image_input = image_input

    def create_image(self) -> Image | None:
        if not self.image_input.url or not self.image_input.provider:
            return None
        db = router.db_for_write(Image)
        img = Image.objects.create(
            url=self.image_input.url,
            provider=self.image_input.provider,
            alt=self.image_input.alt,
            caption=self.image_input.caption
        )
        img.save(using=db)
        return img

    def update_image(self, image: Image) -> Image | None:
        if not self.image_input.url and not self.image_input.provider:
            return None
        if self.image_input.url and image.url:
            if self.image_input.url != image.url:
                cloudinary.uploader.destroy(image.url)
                image.url = self.image_input.url
        image.provider = self.image_input.provider if self.image_input.provider else image.provider
        image.alt = self.image_input.alt if self.image_input.alt else image.alt
        image.caption = self.image_input.caption if self.image_input.caption else image.caption
        image.save()
        return image

    def delete_image(self, image: Image) -> bool:
        if not image:
            return False
        if image.provider == 'cloudinary':
            cloudinary.uploader.destroy(image.url)
        image.delete()
        return True
    
    def auto_image(self) -> Image | None:
        if self.image_input.action == 'create':
            return self.create_image()
        elif self.image_input.action == 'update':
            image = Image.objects.get(pk=self.image_input.id)
            return self.update_image(image)
        elif self.image_input.action == 'delete':
            image = Image.objects.get(pk=self.image_input.id)
            if self.delete_image(image):
                return None
            return None
        elif self.image_input.action == 'none':
            if self.image_input.id:
                return Image.objects.get(pk=self.image_input.id)
            return None
        else:
            return None
        

class ImageUrlBuilder:
    def __init__(self, image: Image):
        self.image = image

    def build_url(self, width=None, height=None, crop=None, quality=None, format=None, effect={}) -> str:
        if self.image.provider == 'cloudinary':
            transformation = [
                {'width': width} if width else None,
                {'height': height} if height else None,
                {'crop': crop or 'scale'},
                {'fetch_format': format or 'auto'},
                {'quality': quality or 'auto'},
                {'effect': effect} if effect else None
            ]
            url = CloudinaryImage(self.image.url).build_url(transformation=transformation)
            return url
        return self.image.url