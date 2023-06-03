# Generated by Django 4.2 on 2023-06-03 15:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_product", "0019_products_expert_products_expert_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="end_auction",
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="products",
            name="start_auction",
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
