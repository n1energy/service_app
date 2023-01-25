from django.contrib import admin

from services.models import Plan, Subscription, Service

admin.site.register(Service)
admin.site.register(Subscription)
admin.site.register(Plan)
