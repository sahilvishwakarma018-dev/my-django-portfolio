from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm

# def home(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST, request.FILES)
#         if form.is_valid():
#             contact = form.save()
            
#             # Send email
#             subject = f'New Portfolio Contact: {contact.name}'
#             body = f"""
#             New contact form submission:
            
#             Name: {contact.name}
#             Email: {contact.email}
#             Message: {contact.message}
#             """
            
#             email = EmailMessage(
#                 subject=subject,
#                 body=body,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 to=[settings.DEFAULT_FROM_EMAIL],
#             )
#             print(settings.DEFAULT_FROM_EMAIL,"-------ddd")
#             print(settings.EMAIL_HOST_USER,"---uuuu")
            
#             if contact.attachment:
#                 email.attach(
#                     contact.attachment.name,
#                     contact.attachment.read(),
#                     'application/pdf'
#                 )
#             try:
#                 email.send(fail_silently=False)
#                 messages.success(request, "✅ Message sent successfully!")
#             except Exception as e:
#                 print("❌ Email sending failed:", e)
#                 messages.error(request, "❌ Failed to send message.")

#             return redirect('home')
#     else:
#         form = ContactForm()
    
#     return render(request, 'portfolio/home.html', {'form': form})



# def home(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST, request.FILES)
#         if form.is_valid():
#             contact = form.save()
            
#             # Send email
#             subject = f'New Portfolio Contact: {contact.name}'
#             body = f"""
#             New contact form submission:
            
#             Name: {contact.name}
#             Email: {contact.email}
#             Message: {contact.message}
#             """
            
#             email = EmailMessage(
#                 subject=subject,
#                 body=body,
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 to=[settings.DEFAULT_FROM_EMAIL],
#             )
#             print(settings.DEFAULT_FROM_EMAIL,"-------ddd")
#             print(settings.EMAIL_HOST_USER,"---uuuu")
            
#             if contact.attachment:
#                 email.attach(
#                     contact.attachment.name,
#                     contact.attachment.read(),
#                     'application/pdf'
#                 )
#             try:
#                 email.send(fail_silently=False)
#                 messages.success(request, "✅ Message sent successfully!")
#             except Exception as e:
#                 print("❌ Email sending failed:", e)
#                 messages.error(request, "❌ Failed to send message.")

#             return redirect('home')
#     else:
#         form = ContactForm()
    
#     return render(request, 'portfolio/home.html', {'form': form})




import base64

from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm

from sib_api_v3_sdk import ApiClient, Configuration
from sib_api_v3_sdk.api.transactional_emails_api import TransactionalEmailsApi
from sib_api_v3_sdk.models import SendSmtpEmail


def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)

        if form.is_valid():
            contact = form.save()

            # 🔐 Configure Brevo
            configuration = Configuration()
            configuration.api_key['api-key'] = settings.BREVO_API_KEY
            api_instance = TransactionalEmailsApi(ApiClient(configuration))

            # 📧 Prepare email
            email = SendSmtpEmail(
                sender={"email": settings.DEFAULT_FROM_EMAIL},
                to=[{"email": settings.DEFAULT_FROM_EMAIL}],
                subject=f"New Portfolio Contact: {contact.name}",
                html_content=f"""
                    <p><b>Name:</b> {contact.name}</p>
                    <p><b>Email:</b> {contact.email}</p>
                    <p><b>Message:</b> {contact.message}</p>
                """
            )

            # 📎 Attachment (optional)
            if contact.attachment:
                email.attachment = [{
                    "name": contact.attachment.name,
                    "content": base64.b64encode(
                        contact.attachment.read()
                    ).decode()
                }]

            try:
                api_instance.send_transac_email(email)
                messages.success(request, "✅ Message sent successfully!")
            except Exception as e:
                print("❌ Email sending failed:", e)
                messages.error(request, "❌ Failed to send message.")

            return redirect('home')

    else:
        form = ContactForm()

    return render(request, 'portfolio/home.html', {'form': form})
