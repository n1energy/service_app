from django.core.validators import MaxValueValidator
from django.db import models

from clients.models import Client
from services.tasks import total_price


class Service(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__price = self.price

    def save(self, *args, **kwargs):
        if self.price != self.__price:
            for subscription in self.subscriptions.all():
                total_price.delay(subscription.id)
        return super().save(*args, **kwargs)


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount')
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

    def __str__(self):
        return f"{self.plan_type}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount = self.discount

    def save(self, *args, **kwargs):
        if self.discount != self.__discount:
            for subscription in self.subscriptions.all():
                total_price.delay(subscription.id)
        return super().save(*args, **kwargs)


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='subscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='subscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)

