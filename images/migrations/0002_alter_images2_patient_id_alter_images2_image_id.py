# Generated by Django 4.0.3 on 2022-03-28 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images2',
            name='Patient_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='images2',
            name='image_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]