# Generated by Django 2.2.6 on 2020-07-19 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room_reservations_TB', '0002_auto_20200719_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_description',
            field=models.TextField(blank=True),
        ),
    ]
