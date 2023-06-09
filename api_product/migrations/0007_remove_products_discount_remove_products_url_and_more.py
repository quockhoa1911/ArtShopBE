# Generated by Django 4.2 on 2023-05-07 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_product', '0006_rename_categories_products_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='products',
            name='url',
        ),
        migrations.AddField(
            model_name='products',
            name='current_price',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='end_auction',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='slug',
            field=models.SlugField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='start_auction',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.CreateModel(
            name='ImageProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('image', models.CharField(blank=True, max_length=256, null=True)),
                ('product', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imageproduct', to='api_product.products')),
            ],
            options={
                'ordering': ('create_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AuctionProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('price_auction', models.CharField(blank=True, default=None, max_length=256, null=True)),
                ('product', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auctionproduct', to='api_product.products')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auctionproduct', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('create_at',),
                'abstract': False,
            },
        ),
    ]
