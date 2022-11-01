# Generated by Django 4.1.2 on 2022-10-31 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.IntegerField(),
        ),
    ]