from django.db.models.signals import post_save
from django.dispatch import receiver

from store.models.users import Address
from .models import User



@receiver(post_save,sender=User)
def create_address(sender,**kwargs):
    user = kwargs.get('instance')
    if kwargs.get('created'):
        Address.objects.create(user=user)