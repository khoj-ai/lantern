# Generated by Django 4.2.2 on 2023-06-16 18:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("beta_product", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userinterest",
            name="unique_identifier",
            field=models.CharField(
                blank=True, default="", max_length=100, null=True, unique=True
            ),
        ),
    ]