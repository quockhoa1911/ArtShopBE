from django.db import migrations


def load_initial_data(apps, schema_editor):
    role_model = apps.get_model('api_auth', 'Role')
    list_role = [
        role_model(name="expert")
    ]

    role_model.objects.bulk_create(list_role)


class Migration(migrations.Migration):
    dependencies = [
        ('api_auth', '0007_expert')
    ]

    operations = [
        migrations.RunPython(load_initial_data)
    ]
