# Generated by Django 3.2.16 on 2022-11-28 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_symptomsshared_prescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedfiles',
            name='digital_signature',
            field=models.CharField(default=1234567890, max_length=512),
            preserve_default=False,
        ),
    ]
