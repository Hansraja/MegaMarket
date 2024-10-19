import graphene
from graphene_django.types import DjangoObjectType

from Common.tools import ImageHandler
from User.types import CustomerInput
from .models import User

class UserObject(DjangoObjectType):
    name = graphene.String()
    email = graphene.String()

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff', 'last_login')
    
    def resolve_name(self, info):
        return self.get_full_name()
    
    def resolve_email(self, info):
        user = info.context.user
        if user.is_anonymous or user.pk != self.pk:
            return None
        return self.email[0] + '*' * (self.email.index('@') - 1) + self.email[self.email.index('@'):]


class NewCustomer(graphene.Mutation):
    class Input:
        input = CustomerInput(required=True)

    customer = graphene.Field(UserObject)

    @staticmethod
    def mutate(root, info, input : CustomerInput | None =None):
        _image = None
        if input.image:
            _image = ImageHandler(input.image).auto_image()
            del input['image']
        user = User.objects.create_user(**input, image=_image)
        return NewCustomer(customer=user)


class Query(graphene.ObjectType):
    users = graphene.List(UserObject)

    def resolve_users(self, info):
        return User.objects.all()

class Mutation(graphene.ObjectType):
    new_customer = NewCustomer.Field()