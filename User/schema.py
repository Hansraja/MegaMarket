from datetime import datetime, timedelta
import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import authenticate
from Common.tools import ImageHandler
from User.Utils.tools import generate_otp
from User.types import CustomerInput
from .models import EmailVerifications, User

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

    user = graphene.Field(UserObject)
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input : CustomerInput | None =None):
        _image = None
        if input.image:
            _image = ImageHandler(input.image).auto_image()
            del input['image']
        user = User.objects.create_user(**input, image=_image)
        return NewCustomer(customer=user, success=True)


class SendVerificationEmail(graphene.Mutation):
    class Input:
        email = graphene.String(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, email):
        otp_code = generate_otp()
        vfc = EmailVerifications.objects.create(email=email, otp=otp_code, expires_at=datetime.now() + timedelta(minutes=10))
        sent = vfc.send_verification_email_otp()
        if not sent:
            return SendVerificationEmail(success=False, message='Failed to send verification email')
        return SendVerificationEmail(success=True, message='Verification email sent')
    
class VerifyEmail(graphene.Mutation):
    class Input:
        email = graphene.String(required=True)
        otp = graphene.String(required=True)
    
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, email, otp):
        vfc = EmailVerifications.objects.filter(email=email, otp=otp, expires_at__gte=datetime.now()).first()
        if not vfc:
            return VerifyEmail(success=False, message='Invalid OTP')
        vfc.delete()
        return VerifyEmail(success=True, message='Email verified')

class UserLogin(graphene.Mutation):
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    
    user = graphene.Field(UserObject)
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, email, password):
        user = User.objects.filter(email=email).first()
        if not user:
            return UserLogin(success=False, message='Invalid email or password')
        if not user.check_password(password):
            return UserLogin(success=False, message='Invalid email or password')
        user = authenticate(email=email, password=password)
        return UserLogin(user=user, success=True, message='Login successful')


class Query(graphene.ObjectType):
    users = graphene.List(UserObject)

    def resolve_users(self, info):
        return User.objects.all()

class Mutation(graphene.ObjectType):
    new_customer = NewCustomer.Field()
    send_verification_email = SendVerificationEmail.Field()
    verify_email = VerifyEmail.Field()
    user_login = UserLogin.Field()