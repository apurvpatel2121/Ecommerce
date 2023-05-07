# Generated by Django 4.1.7 on 2023-05-05 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_variation_product'),
        ('carts', '0003_alter_cartitem_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
