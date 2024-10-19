import graphene

from Common.types import ImageInput

class ItemStatusEnum(graphene.Enum):
    AVAILABLE = "available"
    OUT_OF_STOCK = "out_of_stock"
    COMING_SOON = "comming_soon"
    DISCONTINUED = "discontinued"

class ItemExtraField(graphene.InputObjectType):
    title = graphene.String(required=True)
    type = graphene.String(required=True)
    data = graphene.JSONString(required=True)

class NewItemInput(graphene.InputObjectType):
    sku = graphene.String(required=True)
    name = graphene.String(required=True)
    teaser = graphene.String(required=True)
    description = graphene.String()
    bullet_points = graphene.List(graphene.String)
    image = ImageInput(required=True)
    images = graphene.List(ImageInput)
    tags = graphene.List(graphene.String, required=True)
    status = graphene.Field(ItemStatusEnum)
    price = graphene.Float(required=True)
    delivery_time = graphene.Int()
    shipping_cost = graphene.Float()
    can_return = graphene.Boolean(required=True)
    return_time = graphene.Int()
    return_policy = graphene.String()
    category = graphene.String(required=True)
    vendor =  graphene.String(required=True)
    brand = graphene.String()
    extra_fields = graphene.List(ItemExtraField)