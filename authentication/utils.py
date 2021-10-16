from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .tokens import generate_taken
from adf_bug_tracker.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User


def email_template_message(request, user):
    current_site = get_current_site(request)
    return render_to_string('email_confirmation.html', {
        'username': user.username,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_taken.make_token(user)
    })


def send_email(email_subject, email_message, email_receivers, email_host=EMAIL_HOST_USER):
    email = EmailMessage(
        email_subject,
        email_message,
        email_host,
        email_receivers
    )
    email.fail_silently = True
    email.send()


def activateAccount(uidb64, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except (TypeError, User.DoesNotExist, ValueError, OverflowError):
        user = None

    return (user, generate_taken.check_token(user, token))