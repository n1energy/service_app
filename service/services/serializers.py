from rest_framework import serializers

from services.models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    client_name = serializers.CharField(source="client.company_name")
    email = serializers.CharField(source="client.user.email")

    def get_price():
        return (instance.service.price - instance.service.price * (instance.plan.discount / 100)) 
    
    class Meta:
        model = Subscription
        fields = (
            "id",
            "plan_id",
            "plan",
            "client_name",
            "email",
        )
