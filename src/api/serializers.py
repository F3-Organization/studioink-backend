from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Studio


class CustomRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    studio_name = serializers.CharField(required=True, allow_blank=True)

    def cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "email": self.validated_data.get("email", ""),
            "password": self.validated_data.get("password", ""),
            "studio_name": self.validated_data.get("studio_name", ""),
        }

    def save(self):
        user, studio = self.create(self.validated_data)
        return user, studio

    def create(self, validated_data):
        self.verify_unique_email(validated_data["email"])
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        studio = Studio.objects.create(
            name=validated_data["studio_name"],
            owner=user,
            subscription_plan=Studio.SubscriptionPlan.SOLO,
            subscription_status=Studio.SubscriptionStatus.TRIALING,
        )
        return user, studio

    def verify_unique_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return email
