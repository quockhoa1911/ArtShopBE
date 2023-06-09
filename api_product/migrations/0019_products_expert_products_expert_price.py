# Generated by Django 4.2 on 2023-05-31 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api_auth", "0008_init_data_expert"),
        ("api_product", "0018_alter_products_auction_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="products",
            name="expert",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product",
                to="api_auth.expert",
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="expert_price",
            field=models.FloatField(blank=True, max_length=256, null=True),
        ),
    ]
