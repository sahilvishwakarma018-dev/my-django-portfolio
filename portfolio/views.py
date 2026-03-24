from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
import base64

from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from sib_api_v3_sdk import ApiClient, Configuration
from sib_api_v3_sdk.api.transactional_emails_api import TransactionalEmailsApi
from sib_api_v3_sdk.models import SendSmtpEmail
from gradio_client import Client
from django.http import JsonResponse


def call_chatbot_api(message: str) -> str:
    client = Client("sahil-dev018/Chat-Bot")  # ✅ create client

    try:
        print("Calling API...")
        result = client.predict(
            message=message,
            api_name="/chat"
        )
        return result

    except Exception as e:
        print("Error while calling chatbot:", e)
        raise e

    finally:
        client.close()  # ✅ safe to close


def chatbot_query(request):
    message = request.GET.get('message')

    if not isinstance(message, str) or not message.strip():
        return JsonResponse({"error": "Message text is required."}, status=400)

    try:
        reply = call_chatbot_api(message=message.strip())

    except Exception as exc:
        print("Chatbot proxy error:", exc)
        return JsonResponse(
            {"error": "Assistant is unreachable. Please try again shortly."},
            status=502,
        )

    return JsonResponse({"reply": reply})


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
