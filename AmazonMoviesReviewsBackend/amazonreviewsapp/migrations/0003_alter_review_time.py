# Generated by Django 4.2.8 on 2023-12-09 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazonreviewsapp', '0002_alter_review_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='time',
            field=models.BigIntegerField(),
        ),
    ]
