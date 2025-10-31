from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm

def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save()
            
            # Send email
            subject = f'New Portfolio Contact: {contact.name}'
            message = f"""
            New contact form submission:
            
            Name: {contact.name}
            Email: {contact.email}
            Message: {contact.message}
            """
            
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
            )
            
            try:
                if contact.attachment:
                    email.attach_file(contact.attachment.path)
                email.send()
            except Exception as e:
                print("Email sending failed:", e)
            
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('home')
    else:
        form = ContactForm()
    
    return render(request, 'portfolio/home.html', {'form': form})