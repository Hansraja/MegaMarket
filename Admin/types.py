import graphene

from Common.types import ImageInput


class BannerTypeEnum(graphene.Enum):
    BANNER = 'banner'
    SLIDER = 'slider'

class BannerInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    description = graphene.String()
    image = ImageInput(required=True)
    small_image = ImageInput()
    button = graphene.JSONString()
    position = graphene.String()
    priority = graphene.Int()
    type = BannerTypeEnum(required=True)
    is_active = graphene.Boolean()

class BannerUpdateInput(graphene.InputObjectType):
    title = graphene.String()
    description = graphene.String()
    image = ImageInput()
    small_image = ImageInput()
    button = graphene.JSONString()
    position = graphene.String()
    priority = graphene.Int()
    type = BannerTypeEnum()
    is_active = graphene.Boolean()

class BannerGroupInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    banners = graphene.List(graphene.String, required=True)
    location = graphene.String()
    is_active = graphene.Boolean()

class BannerGroupUpdateInput(graphene.InputObjectType):
    title = graphene.String()
    banners = graphene.List(graphene.String)
    location = graphene.String()
    is_active = graphene.Boolean()