# Generated by Django 2.1.7 on 2019-04-05 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RegistrationModule', '0005_auto_20190405_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginDetails',
            fields=[
                ('username', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=10)),
            ],
        ),
    ]
