# Generated by Django 4.2.1 on 2023-05-23 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_emailverification'),
        ('organizers', '0006_alter_organizer_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizer',
            name='email_verification',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.emailverification'),
        ),
    ]
