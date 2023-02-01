from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch, F, Sum

from clients.models import Client
from services.models import Subscription
from services.serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = (
        Subscription.objects.all()
        .prefetch_related(
            "plan",
            Prefetch(
                "client",
                queryset=Client.objects.all()
                .select_related("user")
                .only("company_name", "user__email"),
            ),
        )
        .annotate(
            price=F("service__price")
            - F("service__price") * F("plan__discount") / 100.00
        )
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        response = super().list(self, request, *args, **kwargs)
        response_data = {"result": response.data}
        response_data["total_price"]=queryset.aggregate(total=Sum('price')).get('total')
        response.data = response_data
        return response
