import graphene

class ImageActionEnum(graphene.Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'

class ImageInput(graphene.InputObjectType):
    id = graphene.String()
    url = graphene.String(required=True)
    provider = graphene.String(required=True)
    alt = graphene.String()
    caption  = graphene.String()
    action = ImageActionEnum(required=True)