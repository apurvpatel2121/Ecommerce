# Generated by Django 4.1.7 on 2023-05-20 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_orderproduct_variation_orderproduct_variation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='orderd',
            new_name='ordered',
        ),
    ]
