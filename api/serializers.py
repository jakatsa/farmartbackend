from rest_framework import serializers
from .models import User, Customer, Farmer, Animal, Orders
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "role", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()  

    class Meta:
        model = Customer
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")  
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()  
            customer = Customer.objects.create(
                user=user, **validated_data
            ) 
            return customer
        else:
            raise serializers.ValidationError(user_serializer.errors)
