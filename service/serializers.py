from rest_framework import serializers
from .models import EmailMessage

class ContactEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailMessage
        fields = ['id', 'name', 'email', 'message', 'sent_at']

    # Standard DRF validation is more concise
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value