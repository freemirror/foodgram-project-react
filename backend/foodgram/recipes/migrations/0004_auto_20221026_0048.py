# Generated by Django 2.2.19 on 2022-10-25 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20221024_2229'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='subscribe',
            constraint=models.UniqueConstraint(fields=('author', 'subscriber'), name='unique_subscribe'),
        ),
    ]
