from api.models import User, Customer, Farmer, Animal,Orders
from api.serializers import (
    UserSerializer,
    FarmerSerializer,
    CustomerSerializer,
    AnimalSerializer,
    OrderSerializer,
)
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnimalViewing(generics.ListCreateAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer


class CustomerRegistrationView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FarmerRegistrationView(APIView):
    def post(self, request):
        serializer = FarmerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentRegistrationView(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete() 
                token = Token.objects.create(user=user)

            response_data = {
                "token": token.key,
                "username": user.username,
                "role": user.role,
            }

            if user.role == "customer":
                customer = (
                    user.customer_account
                )  # Assuming the related name is "student_account"
                if customer is not None:
                    # Add customer data to the response data
                    customer_data = CustomerSerializer(customer).data
                    response_data["data"] = customer_data

            elif user.role == "farmer":
                farmer = (
                    user.farmer_account
                )  # Assuming the related name is "student_account"
                if farmer is not None:
                    # Add farmer data to the response data
                    farmer_data = FarmerSerializer(farmer).data
                    response_data["data"] = farmer_data
            return Response(response_data)
        else:
            return Response(
                {"message": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class AnimalCreationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AnimalSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.headers)
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({"detail": "Successfully logged out."})


class CreateOrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # Infer farmer from the provided animal
            animal = serializer.validated_data["animal"]
            serializer.validated_data["farmer"] = animal.farmer

            # Decrease the available quantity of the animal
            quantity = serializer.validated_data["quantity"]
            animal.available -= quantity
            animal.save()

            # Save the order
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
