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


class FarmerSerializer(serializers.ModelSerializer):
    user = UserSerializer() 

    class Meta:
        model = Farmer
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user") 
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save() 
            farmer = Farmer.objects.create(
                user=user, **validated_data
            )  
            return farmer
        else:
            raise serializers.ValidationError(user_serializer.errors)


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = "__all__"

    def create(self, validated_data):
        
        user = self.context["request"].user

        
        if user.role == "farmer":
            
            if "farmer" not in validated_data:
                raise serializers.ValidationError("A farmer must be specified.")

            
            farmer = validated_data.pop("farmer")
            animal = Animal.objects.create(farmer=farmer, **validated_data)
            return animal
        else:
            
            raise serializers.ValidationError("Only farmers can create animals.")
class OrderSerializer(serializers.ModelSerializer):
    animal_name = serializers.CharField(source='animal.animal_name', read_only=True)
    class Meta:
        model = Orders
        fields = [
            "order_id",
            "customer",
            "animal",
            "quantity",
            "order_status",
            "animal_name"
        ]
       # fields = '__all__'
        
        
    def create(self, validated_data):
        animal = validated_data["animal"]
        print(animal)
        validated_data["order_date"] = timezone.now()
        validated_data["animal_name"] = animal.animal_name
        validated_data["order_status"] = "pending"
        return super().create(validated_data)

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'