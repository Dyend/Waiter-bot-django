# Generated by Django 3.2.9 on 2021-11-17 01:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mesa',
            unique_together={('numero', 'id')},
        ),
    ]
