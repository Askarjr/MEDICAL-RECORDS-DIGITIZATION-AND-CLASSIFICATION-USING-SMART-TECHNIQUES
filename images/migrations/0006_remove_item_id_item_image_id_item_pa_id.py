# Generated by Django 4.0.3 on 2022-03-29 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_remove_item_image_id_remove_item_pa_id_item_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='id',
        ),
        migrations.AddField(
            model_name='item',
            name='Image_id',
            field=models.BigIntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='pa_id',
            field=models.TextField(default=182918182),
            preserve_default=False,
        ),
    ]
