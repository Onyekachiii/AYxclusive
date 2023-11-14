# actions.py
from django.core.mail import send_mail
from django.contrib import messages
from userauths.models import User, Profile

def send_quotation_email(modeladmin, request, queryset):
    for quotation in queryset:
        if not quotation.sent:
            # Send email logic here
            send_mail(
                quotation.email_subject,
                quotation.email_body,
                'ay.exclusive@outlook.com',  # Replace with the business owner's email
                [quotation.user.email],
                fail_silently=False,
            )
            quotation.sent = True
            quotation.save()
            messages.success(request, f'Quotation sent to {User.full_name}')

send_quotation_email.short_description = 'Send selected quotations via email'
