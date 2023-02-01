import time

from celery import shared_task
from celery_singleton import Singleton
from django.db.models import F


@shared_task(base=Singleton)
def total_price(subscription_id):
    from services.models import Subscription
    time.sleep(10)
    subscription = Subscription.objects.filter(id=subscription_id).annotate(
            annotated_price=F("service__price")
            - F("service__price") * F("plan__discount") / 100.00
        ).first()
    subscription.price = subscription.annotated_price
    subscription.save()
