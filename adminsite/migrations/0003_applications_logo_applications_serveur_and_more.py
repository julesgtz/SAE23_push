# Generated by Django 4.2.1 on 2023-06-02 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminsite', '0002_auto_20230602_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='application_logos/'),
        ),
        migrations.AddField(
            model_name='applications',
            name='serveur',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='applications',
            name='utilisateurs',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
