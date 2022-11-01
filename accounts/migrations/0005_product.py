# Generated by Django 4.1.2 on 2022-10-30 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_customuser_mobile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=100)),
                ('pharmacy_name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('address', models.CharField(max_length=150)),
            ],
        ),
    ]
