from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_group(**_kwargs):
    add_activity = Permission.objects.get(codename='add_activity')
    change_activity = Permission.objects.get(codename='change_activity')
    delete_activity = Permission.objects.get(codename='delete_activity')

    group, created = Group.objects.get_or_create(name='staff')
    if created:
        group.permissions.add(add_activity, change_activity, delete_activity)
        group.save()

    group, created = Group.objects.get_or_create(name='admin')
    if created:
        group.permissions.add(add_activity, change_activity, delete_activity)
