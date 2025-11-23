import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

# IMPORT YOUR MODELS HERE - ADJUST THE IMPORT PATH
from account.models import CustomUser
from vendors.models import SellerProfile, Location 

class Command(BaseCommand):
    help = 'Populates the database with 50 Nigerian sellers, businesses, and branches'

    def handle(self, *args, **kwargs):
        # Initialize Faker with Nigerian locale
        fake = Faker('en_NG') 

        self.stdout.write("Seeding database... This might take a few seconds.")

        # We use a transaction to make sure if it fails, we don't get half-data
        with transaction.atomic():
            for _ in range(50):
                # 1. Create User (Seller)
                email = fake.unique.email()
                username = email.split('@')[0] + str(random.randint(1, 999))
                
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',  # Generic password for testing
                    role='seller',
                    first_name=fake.first_name(),
                    last_name=fake.last_name()
                )

                # 2. Create Vendor Profile (Business)
                # I am assuming a OneToOne or ForeignKey relationship to User
                vendor = SellerProfile.objects.create(
                    user=user, 
                    store_name=fake.company(),
                    description=fake.catch_phrase(), # Generates a slogan/description
                    phone_number=fake.phone_number()
                )

                # 3. Create 2-5 Branches for this Vendor
                for _ in range(random.randint(2, 5)):
                    # Generating realistic Lagos-area coordinates (approximate)
                    # Lat: 6.4 to 6.7, Long: 3.3 to 3.5
                    lat = random.uniform(6.4200, 6.7000)
                    lon = random.uniform(3.3000, 3.5000)

                    Location.objects.create(
                        vendor_profile=vendor, # Assuming ForeignKey in Location model
                        address_line1=fake.address(),
                        city=fake.city(),
                        latitude=lat,
                        longitude=lon
                    )

        self.stdout.write(self.style.SUCCESS('Successfully created 50 Sellers with Businesses and Locations!'))