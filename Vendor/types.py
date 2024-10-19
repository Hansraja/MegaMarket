import graphene

from Common.types import ImageInput


class VemdorStoreInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    description = graphene.String(required=True)
    logo = ImageInput(required=True)
    banner = ImageInput()
    address = graphene.String()
    phone = graphene.String()
    email = graphene.String()
    website = graphene.String()

class NewVendorInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    sex = graphene.String()
    dob = graphene.Date()
    image = ImageInput()
    store = VemdorStoreInput(required=True)
