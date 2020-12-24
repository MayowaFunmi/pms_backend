import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from feedback.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Feedback.objects.all())])

    class Meta:
        model = Feedback
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'message']

    def validate(self, attrs):
        email = attrs.get('email', '')
        phone_number = attrs.get('phone_number', '')

        if not re.match(r"(^[0]\d{10}$)|(^[\+]?[234]\d{12}$)", phone_number):
            raise serializers.ValidationError('This phone number is invalid')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise serializers.ValidationError('This email is invalid')

        return attrs

    def create(self, validated_data):
        feedback = Feedback.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            message=validated_data['message']
        )
        feedback.save()
        return feedback
