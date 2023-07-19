from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


class VerifyEmail:
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def _get_verification_url(self):
        """returns email confirmation url
        based on Customer's token"""
        current_site = get_current_site(self.request).domain
        endpoint = reverse("email-verify")
        access_token = self.data["tokens"]["access"]
        absolute_url = f"https://{current_site}{endpoint}?token={access_token}"
        return absolute_url

    def send_verification_email(self) -> None:
        """sends an email to Customer's inbox
        in order to verify an account"""
        email = EmailMessage(
            subject="Email verification",
            body=f"Please, verify your email \n{self._get_verification_url()}",
            to=(self.data["email"],),
        )

        email.send()
