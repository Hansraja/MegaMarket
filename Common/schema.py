import graphene
from graphene_django import DjangoObjectType
from Common.models import Image
from Common.tools import ImageUrlBuilder

class ImageCropEnum(graphene.Enum):
    SCALE = 'scale'
    FILL = 'fill'

class ImageObject(DjangoObjectType):
    public_id = graphene.String()
    blur_url = graphene.String()
    has_image = graphene.Boolean()
    url = graphene.String(
        width=graphene.Int(),
        height=graphene.Int(),
        crop=graphene.Argument(ImageCropEnum),
        quality=graphene.Int(),
        format=graphene.String()
    )

    class Meta:
        model = Image
        fields = ('url', 'id', 'alt', 'caption', 'provider')

    def resolve_url(self, info, width=None, height=None, crop=None, quality=None, format=None, **kwargs):
        if isinstance(self, Image) and self.has_url:
            return self._url
        return ImageUrlBuilder(self).build_url(
            width=width, height=height, crop=crop.value if crop else None, quality=quality, format=format
        )
    
    def resolve_public_id(self, info):
        return self.url
    
    def resolve_has_image(self, info):
        return self.id is not None
    
    def resolve_blur_url(self, info):
        if self.provider == 'cloudinary' and self.url:
            return ImageUrlBuilder(self).build_url(
                width=10, height=10, crop='fill', quality=10, format='webp', effect={'blur': 200}
            )
        return ImageUrlBuilder(Image(url="74f98fbe6a8ada2db6ec26feb98f994e")).build_url(
            width=10, height=10, crop='fill', quality=10, format='webp', effect={'blur': 200}
        )

class Query(graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    pass