# Generated by Django 2.0.7 on 2018-07-25 01:13

from django.db import migrations


def forwards(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group_setups = {
        "admin": {
            "name": "GESTOR",
            "permissions": [
                "can_see_all_files",
                "can_manage_user_information",
                "can_read_usage_information",
                "can_manage_upload_limit",
                "can_change_own_name",
                "can_change_own_email",
            ]},
        "staff": {
            "name": "FUNCIONARIO",
            "permissions": []
        }
    }

    for group_setup in group_setups.values():
        group, _ = Group.objects.get_or_create(name=group_setup['name'])
        group.permissions.set(Permission.objects.filter(codename__in=group_setup['permissions']))


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]