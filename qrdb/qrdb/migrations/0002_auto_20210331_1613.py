# Generated by Django 3.1.7 on 2021-03-31 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qrdb', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review_v1',
            old_name='number',
            new_name='old_id',
        ),
    ]
