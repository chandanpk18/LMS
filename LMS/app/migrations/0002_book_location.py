# Generated by Django 5.0.2 on 2024-05-27 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='location',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
