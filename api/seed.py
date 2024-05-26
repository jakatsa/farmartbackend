import os
from random import choice, randint
import django
import sys
from django.db import transaction

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmartbackend.settings')
django.setup()

from api.models import Farmer, Orders, User, Customer, Animal

def seed():
    # Clear existing data
    User.objects.all().delete()
    Customer.objects.all().delete()
    Farmer.objects.all().delete()
    Animal.objects.all().delete()
    Orders.objects.all().delete()

    # Create users
    user1 = User(username='farmer1', role='farmer', first_name='Alex', last_name='Kimeu', email='alex@gmail.com')
    user1.set_password('password123')  # Set a password if needed
    user1.save()

    user2 = User(username='customer1', role='customer', first_name='John', last_name='Gitu', email='john@gmail.com')
    user2.set_password('james123')
    user2.save()

    # Create a customer
    customer1 = Customer(profile_picture='image.png', user=user2)
    customer1.save()

    # Create a farmer
    farmer1 = Farmer(profile_picture='image.png', user=user1, contact='123456789')
    farmer1.save()

    # Detailed list of animals with specific image URLs
    animals_data = [
        {'type': 'Bull', 'species': 'Cattle', 'gender': 'Male', 'breed': 'Belgian Blue', 'image': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRtTB41MVOoRhNJ8oyzOSRRYYVF5_jFq-Bhk5cqkqjmnocnxMYv', 'age': 60, 'category': 'Meat'},
        {'type': 'Bull', 'species': 'Cattle', 'gender': 'Male', 'breed': 'Hereford', 'image': 'https://upload.wikimedia.org/wikipedia/commons/c/cf/Hereford_bull_in_a_field_by_the_B4452_%28cropped%29.jpg', 'age': 70, 'category': 'Meat'},
        {'type': 'Bull', 'species': 'Cattle', 'gender': 'Male', 'breed': 'Brown Swiss', 'image': 'https://cdn.standardmedia.co.ke/images/wysiwyg/images/HO3sM1KpgJNNPbOsBYJC0H0TfxXTF1XE3b6PcMnl.jpg', 'age': 44, 'category': 'Meat'},
        {'type': 'Cow', 'species': 'Cattle', 'gender': 'Female', 'breed': 'Holstein Friesian', 'image': 'https://t0.gstatic.com/licensed-image?q=tbn:ANd9GcQ-3VPFpWVE8NMzQayUEgyBphcFlo63Mtt-zO7uV_YpHRRXl1sDydGmXR48APxLL1BY', 'age': 50, 'category': 'dairy'},
        {'type': 'Cow', 'species': 'Cattle', 'gender': 'Female', 'breed': 'Jersey', 'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Bou%C3%ABts_d%27J%C3%A8rri_%C3%8Agypte_5_J%C3%A8rri_Mai_2009.jpg/1200px-Bou%C3%ABts_d%27J%C3%A8rri_%C3%8Agypte_5_J%C3%A8rri_Mai_2009.jpg', 'age': 39, 'category': 'dairy'},
        {'type': 'Cow', 'species': 'Cattle', 'gender': 'Female', 'breed': 'Guernsey', 'image': 'https://cdn.britannica.com/20/520-050-A5A47504/Guernsey-cow.jpg', 'age': 45, 'category': 'dairy'},
        {'type': 'Goat', 'species': 'Goat', 'gender': 'Male', 'breed': 'Pygmy', 'image': 'https://hips.hearstapps.com/hmg-prod/images/black-goat-sit-royalty-free-image-1633534925.jpg?crop=0.668xw:1.00xh;0.162xw,0&resize=980:*', 'age': 16, 'category': 'Meat'},
        {'type': 'Goat', 'species': 'Goat', 'gender': 'Male', 'breed': 'Toggenburg', 'image': 'https://upload.wikimedia.org/wikipedia/commons/1/15/Toggenburgerbok.jpg', 'age': 30, 'category': 'Meat'},
        {'type': 'Goat', 'species': 'Goat', 'gender': 'Male', 'breed': 'Carpathian', 'image': 'https://i.pinimg.com/originals/10/45/a5/1045a5c4c4598f60f7935cd889c47d1b.jpg', 'age': 43, 'category': 'Meat'},
        {'type': 'Goat', 'species': 'Goat', 'gender': 'Female', 'breed': 'Nigerian Dwarf', 'image': 'https://upload.wikimedia.org/wikipedia/commons/a/ac/NigerianDwarfDairyGoat.jpg', 'age': 26, 'category': 'Dairy'},
        {'type': 'Goat', 'species': 'Goat', 'gender': 'Female', 'breed': 'Laoshan', 'image': 'https://1.bp.blogspot.com/-SPBYWwbk208/V61gKUgzDBI/AAAAAAAACTk/iDkQi6riJnYOorV6tyAOPgzf_6sfEe-mACLcB/s600/Laoshan%2BGoat.jpg', 'age': 20, 'category': 'Dairy'},
        {'type': 'Goat', 'species': 'Goat', 'gender': 'Female', 'breed': 'LaMancha', 'image': 'https://cdn.britannica.com/33/533-050-2ED3D8DF/LaMancha-goat.jpg', 'age': 38, 'category': 'Dairy'},
        {'type': 'Donkey', 'species': 'Donkey', 'gender': 'Male', 'breed': 'Contentin', 'image': 'https://alchetron.com/cdn/cotentin-donkey-fb252359-9b3d-4d17-9475-49c1a644d27-resize-750.jpg', 'age': 27, 'category': 'Work'},
        {'type': 'Donkey', 'species': 'Donkey', 'gender': 'Male', 'breed': 'Amiatina', 'image': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSOJEiyMB7eqJ47zLP-3mudv6uIeOiVRnDM-P5oDvnZR8LCEUsq', 'age': 18, 'category': 'Work'},
        {'type': 'Donkey', 'species': 'Donkey', 'gender': 'Male', 'breed': 'Corsican', 'image': 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcReKJE_TtX_EFtMDfJ3o9zlb3THU29XeNAFPfz1YIHuYI-vnSrt', 'age': 21, 'category': 'Work'},
        {'type': 'Donkey', 'species': 'Donkey', 'gender': 'Male', 'breed': 'Somali wild', 'image': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQM2nWPIUA_kfAHwgGTknlDPVM2sLtX0_IEnLhNMeHg9rGmWOCu', 'age': 7, 'category': 'Work'},
        {'type': 'Sheep', 'species': 'Sheep', 'gender': 'Male', 'breed': 'Shropshire', 'image': 'https://images.saymedia-content.com/.image/t_share/MTc3MzIxMjE3OTY1OTU4MzA1/15-best-sheep-breeds-for-meat.jpg', 'age': 46, 'category': 'Meat'},
        {'type': 'Sheep', 'species': 'Sheep', 'gender': 'Male', 'breed': 'Bardoka', 'image': 'https://c02.purpledshub.com/uploads/sites/47/2022/11/GettyImages-1467165874-b1f09df.jpg?webp=1&w=1200', 'age': 58, 'category': 'Meat'},
        {'type': 'Sheep', 'species': 'Sheep', 'gender': 'Male', 'breed': 'Texel', 'image': 'https://www.livestockoftheworld.com/uploads/208856bluetexelsheep.jpg', 'age': 50, 'category': 'Meat'},
        {'type': 'Sheep', 'species': 'Sheep', 'gender': 'Female', 'breed': 'Dropper', 'image': 'https://www.cabidigitallibrary.org/cms/10.1079/cabicompendium.85268/asset/70a34f3e-09f1-4772-9e10-e26f91c286a3/assets/graphic/dorper3.jpeg', 'age': 39, 'category': 'Dairy'},
        {'type': 'Goose', 'species': 'Poultry', 'gender': 'Female', 'breed': 'Cackling', 'image': 'https://www.allaboutbirds.org/guide/assets/photo/59950661-480px.jpg', 'age': 16, 'category': 'Layers'},
        {'type': 'Goose', 'species': 'Poultry', 'gender': 'Male', 'breed': 'Barnacle', 'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfdY9nBMO1Ak2gZxyQYeE71SCTnTKJxZ5a8YBYy9iW7Q&s', 'age': 10, 'category': 'Meat'},
        {'type': 'Goose', 'species': 'Poultry', 'gender': 'Male', 'breed': 'Spur-winged', 'image': 'https://ferrebeekeeper.wordpress.com/wp-content/uploads/2016/09/0pp3q8xpykg1rws3iozakn5hfdy2czj_2e2sy2ubibxs.jpg?w=584', 'age': 19, 'category': 'Meat'},
        {'type': 'Chicken', 'species': 'Poultry', 'gender': 'Male', 'breed': 'Ayam Cemani', 'image': 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRh0VQp2K1sETBfSVUKmHUoFjRXCwcToob46rrgUcZaYqe_fzj8', 'age': 29, 'category': 'Meat'},
        {'type': 'Chicken', 'species': 'Poultry', 'gender': 'Male', 'breed': 'Rhode Island Red', 'image': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRACQ5BUONpSK3dkWFbEr0LA4M6pZDu93vRVV30dFE5JLGuzJ4H', 'age': 16, 'category': 'Meat'},
        {'type': 'Chicken', 'species': 'Poultry', 'gender': 'Male', 'breed': 'White Leghorn', 'image': 'https://assets.thechickhatchery.com/thechickhatche/wp-content/uploads/2023/03/19195652/White-Leghorn-Chicken.jpg', 'age': 9, 'category': 'Meat'},
        {'type': 'Chicken', 'species': 'Poultry', 'gender': 'Female', 'breed': 'Brahma', 'image': 'https://upload.wikimedia.org/wikipedia/commons/c/c5/Brahmahahn_%28cropped%29.png', 'age': 23, 'category': 'Layers'},
        {'type': 'Turkey', 'species': 'Poultry', 'gender': 'Male', 'breed': 'Broad Breasted White', 'image': 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTTU1T5fsStE1-qK23cLvPizItW99_B_-W6khQbz4FtPTc5e3zOnva33sesoCCaMDxSziwNcA', 'age': 19, 'category': 'Meat'},
        {'type': 'Turkey', 'species': 'Poultry', 'gender': 'Male', 'breed': 'Bronze Turkey', 'image': 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcRQqu7O43H3ERqEsMUR0Zb_FAmRFG5bTX-XlHQTzs_QqbYvNd8rrxeOAjR5nMDHJTDtG9sv4g', 'age': 22, 'category': 'Meat'},
        {'type': 'Camel', 'species': 'Camel', 'gender': 'Male', 'breed': 'Kharai', 'image': 'https://www.leafconagro.com/wp-content/uploads/Kharai-M.jpg', 'age': 46, 'category': 'Work'},
        {'type': 'Camel', 'species': 'Camel', 'gender': 'Male', 'breed': 'Majaheem', 'image': 'https://www.researchgate.net/publication/313904789/figure/fig1/AS:527717650579456@1502829100412/Majaheem-Saudi-Arabia.png', 'age': 49, 'category': 'Work'},
    ]

    animal_locations = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Thika', 'Nyeri', 'Meru', 'Machakos', 'Embu']

    animal_objects = []

    for data in animals_data:
        animal = Animal(
            animal_picture=data['image'],
            animal_name=data['type'],
            animal_type=data['species'],
            animal_age=data['age'],
            animal_location=choice(animal_locations),
            animal_breed=data['breed'],
            animal_gender=data['gender'],
            animal_category=data['category'],
            available=randint(1, 10),
            farmer=farmer1,
            animal_price=randint(300, 1500),
            animal_description=f'Healthy {data["type"].lower()}'
        )
        animal_objects.append(animal)

    with transaction.atomic():
        Animal.objects.bulk_create(animal_objects)

    print("Seed data added successfully!")

if __name__ == '__main__':
    seed()
