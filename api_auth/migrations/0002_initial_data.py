from django.db import migrations
from django.contrib.auth.hashers import make_password
from django.conf import settings


def load_initial_data(apps, schema_editor):
    role_model = apps.get_model('api_auth', 'Role')
    user_model = apps.get_model('api_auth', 'User')
    role_admin = role_model(name="admin")
    list_role = [
        role_admin,
        role_model(name="user"),
        role_model(name="author")
    ]

    role_model.objects.bulk_create(list_role)

    user_model.objects.create(email=settings.EMAIL_DEFAULT,
                              password=make_password(settings.PASSWORD_DEFAULT), role=role_admin)


class Migration(migrations.Migration):
    dependencies = [
        ('api_auth', '0001_initial')
    ]

    operations = [
        migrations.RunPython(load_initial_data)
    ]
