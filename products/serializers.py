from rest_framework import serializers
from .models import Product
from stock.models import Stock

class ProductSerializer(serializers.ModelSerializer):
    added_by_name = serializers.CharField(source='added_by.full_name', read_only=True)
    stocks = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'purchase_price', 'selling_price', 'photo', 'added_by', 'added_by_name', 'created_at', 'updated_at', 'stocks')
        read_only_fields = ('added_by', 'created_at', 'updated_at')

    def get_stocks(self, obj):
        return [{'size': s.size, 'quantity': s.quantity} for s in obj.stocks.all()]

    def validate_purchase_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена закупки должна быть положительной.")
        return value

    def validate_selling_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена продажи должна быть положительной.")
        return value

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'purchase_price', 'selling_price', 'photo')

    def validate(self, data):
        if data.get('purchase_price', 0) <= 0:
            raise serializers.ValidationError({"purchase_price": "Цена закупки должна быть положительной."})
        if data.get('selling_price', 0) <= 0:
            raise serializers.ValidationError({"selling_price": "Цена продажи должна быть положительной."})
        return data