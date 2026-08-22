from django.db.models.signals import post_save
from django.dispatch import receiver

from catalog.models import Customer, Product

from .models import SyncChange


@receiver(post_save, sender=Customer)
def record_customer_change(sender, instance, **kwargs):
    SyncChange.objects.get_or_create(
        entity_type="customer",
        entity_id=instance.id,
        version=instance.version,
    )


@receiver(post_save, sender=Product)
def record_product_change(sender, instance, **kwargs):
    SyncChange.objects.get_or_create(
        entity_type="product",
        entity_id=instance.id,
        version=instance.version,
    )
