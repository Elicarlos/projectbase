# Generated by Django 5.2.4 on 2025-07-15 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Customer",
        ),
    ]
