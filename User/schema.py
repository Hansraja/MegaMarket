from datetime import datetime, timedelta
from email import message
import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import authenticate, login
from nanoid import generate
from Common.tools import ImageHandler
from User.Utils.tools import generate_otp
from User.types import CustomerInput
from .models import EmailVerifications, User

class UserObject(DjangoObjectType):
    name = graphene.String()
    email = graphene.String()

    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_staff')
    
    def resolve_name(self, info):
        return self.get_full_name()
    
    def resolve_email(self, info):
        user = info.context.user
        if user.is_anonymous or user.pk != self.pk:
            return self.email[0] + '*' * (self.email.index('@') - 1) + self.email[self.email.index('@'):]
        return self.email


class NewCustomer(graphene.Mutation):
    class Input:
        input = CustomerInput(required=True)

    user = graphene.Field(UserObject)
    message = graphene.String()
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, input : CustomerInput | None =None):
        user = User.objects.get(email=input.email)
        if not user:
            return NewCustomer(user=None, success=False, message='Invalid email')
        if user.is_active:
            return NewCustomer(user=None, success=False, message='User already exists')
        _image = None
        if input.image:
            _image = ImageHandler(input.image).auto_image()
        user.set_password(input.password)
        user.first_name = input.first_name
        user.last_name = input.last_name
        user.username = input.username or user.username
        user.dob = input.dob or None
        user.sex = input.sex or None
        user.image = _image or user.image
        user.is_active = True
        user.save()
        return NewCustomer(user=user, success=True, message="Your account has been created")

class CreateNewCustomer(graphene.Mutation):
    class Input:
        email = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserObject)

    @classmethod
    def mutate(cls, root, info, email: str):
        user = User.objects.filter(email=email).first()
        if user and user.is_active:
            return CreateNewCustomer(success=False, message='A user with this email already exists')
        otp_code = generate_otp()
        vfc = EmailVerifications.objects.create(email=email, otp=otp_code, expires_at=datetime.now() + timedelta(minutes=10))
        sent = vfc.send_verification_email_otp()
        if not sent:
            return CreateNewCustomer(success=False, message='Failed to send verification email')
        if not user:
            _username = email[:4] + generate(alphabet="0123456789abcdefghijklmnopqrst",size=8)
            user = User.objects.create(email=email, username=_username, is_active=False)
        return CreateNewCustomer(success=True, user=user, message='Verification email sent')

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
        identifier = graphene.String(required=True)
        password = graphene.String(required=True)
    
    user = graphene.Field(UserObject)
    session_id = graphene.String()
    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, identifier, password):
        print(root, info)
        isEmail = '@' in identifier
        user = User.objects.filter(email=identifier).first() if isEmail else User.objects.filter(username=identifier).first()
        if not user:
            return UserLogin(success=False, message='Invalid credentials')
        if not user.check_password(password):
            return UserLogin(success=False, message='Invalid credentials')
        user = authenticate(email=user.email, password=password)
        login(info.context, user)
        return UserLogin(user=user, success=True, session_id=info.context.session.session_key, message="You have been logged in")


class Query(graphene.ObjectType):
    users = graphene.List(UserObject)
    me = graphene.Field(UserObject)

    def resolve_users(self, info):
        return User.objects.all()
    
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            return None
        return user

class Mutation(graphene.ObjectType):
    new_customer = NewCustomer.Field()
    create_new_customer = CreateNewCustomer.Field()
    send_verification_email = SendVerificationEmail.Field()
    verify_email = VerifyEmail.Field()
    user_login = UserLogin.Field()