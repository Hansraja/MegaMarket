from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_verification_email_otp(email, otp):
    context = {
        "receiver_name": "User",
        "otp_code": otp,
    }

    receiver_email = email
    template_name = "email/otp.html"
    convert_to_html_content =  render_to_string(
      template_name=template_name,
      context=context
    )

    plain_message = strip_tags(convert_to_html_content)

    sent = send_mail(
      subject="Email Verification OTP",
      message=plain_message,
      from_email=settings.EMAIL_HOST_USER,
      recipient_list=[receiver_email,]  ,
      html_message=convert_to_html_content,
      fail_silently=True  
    )

    return sent


def generate_otp():
    import random
    return random.randint(100000, 999999)