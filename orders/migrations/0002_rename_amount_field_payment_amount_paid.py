# Generated by Django 4.1.7 on 2023-05-19 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='amount_field',
            new_name='amount_paid',
        ),
    ]