import graphene
from Common.types import ImageInput


class CustomerInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    sex = graphene.String()
    dob = graphene.Date()
    image = ImageInput()