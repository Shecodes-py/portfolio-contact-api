from django.http import HttpResponse
from rest_framework import generics

from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import ContactEmailSerializer
from .models import EmailMessage

import os 
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logging = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return HttpResponse("Hey there, i see you are checking out this service, head to \"/api/contact\" endpoint to send me a message!")

class ContactEmail(generics.ListCreateAPIView):
    logging.info("Contact Email view initialized")
    queryset = EmailMessage.objects.all()
    serializer_class = ContactEmailSerializer

    def perform_create(self, serializer): 
        instance = serializer.save()
        logging.info(f"Saved EmailMessage instance: {instance}")

        try:            
            data = serializer.validated_data
            # Prepare the email content
            email_content = f"Name: {data['name']}\nEmail: {data['email']}\n\nMessage:\n{data['message']}"
            
            message = Mail(
                    from_email=settings.DEFAULT_FROM_EMAIL, # Use a verified sender
                    to_emails="udotongpeace@gmail.com",
                    subject=f"New Portfolio Message from {data['name']}",
                    plain_text_content=email_content
                )
            logging.info(f"Prepared email message: {message}")
                
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            logging.info(f"SendGrid response status: {response.status_code}")
            if response.status_code not in [200, 202]:
                logging.error(f"Failed to send email via SendGrid: {response.status_code} - {response.body}")
                raise Exception("Failed to send email")
            
        except Exception as e:
            logging.error(f"Contact form error: {str(e)}")
            return Response(
                {"error": "Internal server error"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
