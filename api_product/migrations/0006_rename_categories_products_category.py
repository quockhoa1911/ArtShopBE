# Generated by Django 4.2 on 2023-05-07 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_product', '0005_alter_category_create_at_alter_products_create_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='categories',
            new_name='category',
        ),
    ]
