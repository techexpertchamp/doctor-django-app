# Generated by Django 4.0.4 on 2022-05-17 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0005_alter_patients_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='email',
            field=models.EmailField(max_length=255),
        ),
    ]
