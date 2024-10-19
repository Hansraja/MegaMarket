import graphene

from Api import relay
from Common.tools import ImageHandler
from User.models import User
from Vendor.types import NewVendorInput
from .models import Vendor
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

class VendorObject(DjangoObjectType):
    
    class Meta:
        model = Vendor
        fields = '__all__'
        filter_fields = {
            'name': ['exact', 'icontains'],
            'key': ['exact', 'icontains'],
        }
        interfaces = (relay.Node, )
        use_connection = True


class NewVendor(graphene.Mutation):

    class Input:
        input = NewVendorInput(required=True)

    vendor = graphene.Field(VendorObject)
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input: NewVendorInput | None = None):
        user = User.objects.create_user(
            username=input.username,
            first_name=input.first_name,
            last_name=input.last_name,
            email=input.email,
            password=input.password,
            dob = input.dob,
            sex = input.sex
        )
        if input.image:
            user.image = ImageHandler(input.image).auto_image()
            user.save()
        vendor = Vendor(
            user=user,
            name=input.store.name,
            description=input.store.description,
            logo=ImageHandler(input.store.logo).auto_image(),
            banner=ImageHandler(input.store.banner).auto_image(),
            address=input.store.address,
            phone=input.store.phone,
            email=input.store.email,
            website=input.store.website
        )
        return NewVendor(vendor=vendor, success=True)


class Query:
    vendor = relay.Node.Field(VendorObject)
    vendors = DjangoFilterConnectionField(VendorObject)
    

class Mutation:
    new_vendor = NewVendor.Field()