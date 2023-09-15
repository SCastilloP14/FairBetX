from rest_framework import serializers
from .models import Trade

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = "__all__"
        fields = ("ticker", "quantity", "price", "timestamp")


class CustomTradeSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    open = serializers.DecimalField(max_digits=10, decimal_places=2)
    high = serializers.DecimalField(max_digits=10, decimal_places=2)
    low = serializers.DecimalField(max_digits=10, decimal_places=2)
    close = serializers.DecimalField(max_digits=10, decimal_places=2)
    
