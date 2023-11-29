from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailTemplate

def send_custom_email(user_email, template_subject, context=None):
    email_template = EmailTemplate.objects.get(subject=template_subject)

    subject = email_template.subject
    html_message = render_to_string('custom_email_template.html', {'email_content': email_template.message, 'context': context})
    plain_message = strip_tags(html_message)

    email = EmailMessage(
        subject,
        plain_message,
        'ayexclusive1@outlook.com',  # Replace with your sending email address
        [user_email],
    )

    if email_template.attachment:
        email.attach_file(email_template.attachment.path)

    email.attach_alternative(html_message, "text/html")
    email.send()
