from rest_framework import serializers
from .models import Stock
from products.models import Product

class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Stock
        fields = ('id', 'product', 'product_name', 'size', 'quantity', 'updated_at')
        read_only_fields = ('updated_at',)

    def validate_size(self, value):
        if not (35 <= value <= 42):
            raise serializers.ValidationError("Размер должен быть от 35 до 42.")
        return value

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Количество не может быть отрицательным.")
        return value

    def validate(self, data):
        product = data.get('product')
        if product and not Product.objects.filter(id=product.id).exists():
            raise serializers.ValidationError({"product": "Товар не найден."})
        return data