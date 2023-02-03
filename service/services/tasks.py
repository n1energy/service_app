import datetime
import time

from django.core.cache import cache
from celery import shared_task
from celery_singleton import Singleton
from django.conf import settings
from django.db import transaction
from django.db.models import F


@shared_task(base=Singleton)
def total_price(subscription_id):
    from services.models import Subscription
    with transaction.atomic():
        subscription = Subscription.objects.select_for_update().filter(id=subscription_id).annotate(
            annotated_price=F("service__price")
                            - F("service__price") * F("plan__discount") / 100.00
        ).first()
        subscription.price = subscription.annotated_price
        subscription.save()
    cache.delete(settings.PRICE_CACHE_NAME)


@shared_task(base=Singleton)
def set_description(subscription_id):
    from services.models import Subscription
    with transaction.atomic():
        time.sleep(27)
        subscription = Subscription.objects.select_for_update().get(id=subscription_id)
        subscription.description = str(datetime.datetime.now())
        subscription.save()
    cache.delete(settings.PRICE_CACHE_NAME)
