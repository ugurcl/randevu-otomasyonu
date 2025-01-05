from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from User.models import UserProfile,Institution,TitleModel
from Appointments.models import AppointmentCreation
import random
from datetime import date, time
fake = Faker()

class Command(BaseCommand):
    help = "Generate users"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="Number of users to create")

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        for i in range(count):
            username = fake.user_name()
            email = fake.email()
            password = "default_password123"
            first_name = fake.first_name()
            last_name = fake.last_name()
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'password': password,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

            if created:  
                institution = Institution.objects.order_by('?').first()
                title = TitleModel.objects.order_by('?').first()
                image_list = [5, 13, 19, 21, 23, 66,31,25, 1, 4, 60]
                UserProfile.objects.filter(
                    user=user
                ).update(
                    is_active=True,
                    is_verified=True,
                    bio=fake.text(max_nb_chars=200),
                    contact_email=email,
                    title=title,
                    institution=institution,
                    profile_picture=f"profile_pictures/{random.choice(image_list)}.jpg",
                )
                
                AppointmentCreation.objects.create(
                    staff_member= UserProfile.objects.order_by('?').first(),
                    appointment_is_active=True,
                    date=date(random.randint(2025, 2026), random.randint(1, 10), random.randint(1, 30)),
                    time=time(random.randint(1, 20), 00),
                    
                )

                self.stdout.write(self.style.SUCCESS(f"Kullanıcı ve profil oluşturuldu: {username}"))
            else:
                self.stdout.write(self.style.WARNING(f"Kullanıcı zaten mevcut: {username}"))
