# Generated by Django 4.1.5 on 2023-01-14 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0002_alter_dogpic_modified_alter_dogpic_original'),
    ]

    operations = [
        migrations.AddField(
            model_name='dogpic',
            name='metadata',
            field=models.JSONField(default={}),
        ),
    ]
