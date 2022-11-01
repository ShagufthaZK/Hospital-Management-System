# Generated by Django 4.1.2 on 2022-11-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_cart_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceClaim',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user', models.IntegerField()),
                ('amount', models.FloatField(default=0)),
                ('claimed', models.BooleanField(default=False)),
            ],
        ),
    ]
