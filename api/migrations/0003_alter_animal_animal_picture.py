# Generated by Django 4.2.13 on 2024-05-26 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_orders_animal_name_alter_animal_animal_age"),
    ]

    operations = [
        migrations.AlterField(
            model_name="animal",
            name="animal_picture",
            field=models.CharField(),
        ),
    ]