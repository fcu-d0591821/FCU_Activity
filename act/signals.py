from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.management import create_permissions

@receiver(post_migrate)
def create_group(apps, **_kwargs):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    add_activity = Permission.objects.get(codename='add_activity')
    change_activity = Permission.objects.get(codename='change_activity')
    delete_activity = Permission.objects.get(codename='delete_activity')

    group, created = Group.objects.get_or_create(name='staff')
    if created:
        group.permissions.add(add_activity, change_activity, delete_activity)

    group, created = Group.objects.get_or_create(name='admin')
    if created:
        group.permissions.add(add_activity, change_activity, delete_activity)
