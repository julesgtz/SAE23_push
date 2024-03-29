# Generated by Django 4.2.2 on 2023-06-12 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminsite', '0007_alter_applications_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='serveurs',
            name='stockage_initial',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='applications',
            name='logo',
            field=models.ImageField(blank=True, default='images/applications_default.jpg', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='serveurs',
            name='processeur',
            field=models.IntegerField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='memoire_vive',
            field=models.CharField(max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='services',
            name='stockage_use',
            field=models.CharField(max_length=18, null=True),
        ),
    ]
