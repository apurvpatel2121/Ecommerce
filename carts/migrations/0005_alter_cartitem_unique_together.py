# Generated by Django 4.1.7 on 2023-05-06 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_cartitem_variations'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together=set(),
        ),
    ]