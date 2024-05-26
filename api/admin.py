from django.contrib import admin
from django.contrib import admin
from .models import Farmer, Customer, User, Animal,Orders

# Register your models here.
admin.site.register(Farmer)
admin.site.register(Customer)
admin.site.register(User)
admin.site.register(Animal)
admin.site.register(Orders)