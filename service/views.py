from django.http import HttpResponse
from rest_framework import generics
from .models import EmailMessage
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import ContactEmailSerializer


import os
import logging
from sendgrid.helpers.mail import Email, To, Content, HtmlContent
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logging = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return HttpResponse("Hey there, i see you are checking out this service, head to \"/api/contact\" endpoint to send me a message!")

class ContactEmail(generics.GenericAPIView):
    serializer_class = ContactEmailSerializer

    def post(self, request): 
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            logging.info(f"Validated data: {data}")
            try:
                logging.info(f"Contact form submission: {data}")
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

                if response.status_code in [200, 201, 202]:
                    serializer.save() # Uses the standard DRF save method
                    return Response(
                        {"message": "Email sent and message saved successfully!"}, 
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {"error": "Failed to send email via provider"}, 
                        status=status.HTTP_502_BAD_GATEWAY
                    )

            except Exception as e:
                logging.error(f"Contact form error: {str(e)}")
                return Response(
                    {"error": "Internal server error"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)