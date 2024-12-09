# Generated by Django 4.2.8 on 2023-12-26 11:10

from django.db import migrations
import random

def populate_users(apps, schema_editor):
    countries = apps.get_model('places', 'Country').objects.all().iterator(chunk_size=1000)
    users = apps.get_model('places', 'CustomUser').objects.all()

    for country in countries:
        random_user = random.choice(users)
        country.my_user = random_user
        country.save()


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
         migrations.RunPython(populate_users),
    ]
