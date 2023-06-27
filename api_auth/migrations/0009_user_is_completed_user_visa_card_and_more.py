# Generated by Django 4.2 on 2023-06-20 14:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_auth", "0008_init_data_expert"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="visa_card",
            field=models.CharField(blank=True, default=None, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name="expert",
            name="birthday",
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]