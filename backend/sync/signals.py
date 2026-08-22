from django.db.models.signals import post_save
from django.dispatch import receiver

from catalog.models import Customer, Product
from fulfillment.models import Invoice
from payments.models import CommissionMovement, PaymentReport
from returns.models import ReturnReport
from sales.models import Order
from settlements.models import CommissionSettlement

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


def record_seller_change(instance, entity_type, seller_id, version):
    SyncChange.objects.get_or_create(
        entity_type=entity_type, entity_id=instance.id, version=version,
        defaults={"seller_id": seller_id},
    )


@receiver(post_save, sender=Order)
def record_order_change(sender, instance, **kwargs):
    record_seller_change(instance, "order", instance.seller_id, instance.version)


@receiver(post_save, sender=Invoice)
def record_invoice_change(sender, instance, **kwargs):
    record_seller_change(instance, "invoice", instance.seller_id, instance.version)


@receiver(post_save, sender=PaymentReport)
def record_payment_change(sender, instance, **kwargs):
    record_seller_change(instance, "payment", instance.seller_id, instance.version)


@receiver(post_save, sender=ReturnReport)
def record_return_change(sender, instance, **kwargs):
    record_seller_change(instance, "return", instance.seller_id, instance.version)


@receiver(post_save, sender=CommissionMovement)
def record_commission_change(sender, instance, **kwargs):
    record_seller_change(instance, "commission", instance.seller_id, instance.version)


@receiver(post_save, sender=CommissionSettlement)
def record_settlement_change(sender, instance, **kwargs):
    record_seller_change(instance, "settlement", instance.seller_id, 1)
