import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmartbackend.settings')
django.setup()

from api.models import Farmer, Orders, User, Customer, Animal

def seed():
    # Create a user with role 'farmer'
    User.objects.all().delete()
    Customer.objects.all().delete()
    Farmer.objects.all().delete()
    Animal.objects.all().delete()
    Orders.objects.all().delete()

    user1 = User(username='farmer2', role='farmer', first_name='Alex', last_name='Kimeu', email='alex@gmail.com')
    user1.set_password('password123')  # Set a password if needed
    # user2 = User(username="")
    user1.save()

    # Create a customer with a profile picture
    customer1 = Customer(profile_picture='image.png', user=user1)
    customer1.save()

    # Create a farmer with a profile picture and contact info
    farmer1 = Farmer(profile_picture='image.png', user=user1, contact='123456789')
    farmer1.save()

    # Create an animal associated with the farmer
    animal1 = Animal(
        animal_picture='animal.png',
        animal_name='Cow',
        animal_type='Milk Animal',
        animal_age='2 years',
        animal_location='Kiambu',
        animal_breed='Holstein',
        available=1,
        farmer=farmer1,
        animal_price=500,
        animal_description='Healthy cow'
    )
    animal1.save()

    animal2 = Animal(
        animal_picture='animal.png',
        animal_name='Chicken',
        animal_type='Poultry',
        animal_age='2 years',
        animal_location='Nyeri',
        animal_breed='Araucana',
        available=4,
        farmer=farmer1,
        animal_price=500,
        animal_description='Healthy chicken'
    )
    animal2.save()

    print("Seed data added successfully!")

if __name__ == '__main__':
    seed()