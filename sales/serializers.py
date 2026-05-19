from rest_framework import serializers
from .models import Sale
from stock.models import Stock
from users.models import User
from products.models import Product

class SaleSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    seller_name = serializers.CharField(source='seller.full_name', read_only=True)
    
    class Meta:
        model = Sale
        fields = ('id', 'product', 'product_name', 'customer', 'customer_name', 
                  'seller', 'seller_name', 'size', 'quantity', 'price', 
                  'payment_method', 'created_at')
        read_only_fields = ('price', 'created_at', 'seller')

class SaleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ('product', 'customer', 'size', 'quantity', 'payment_method')
    
    def validate(self, data):
        product = data['product']
        size = data['size']
        quantity = data['quantity']
        
        try:
            stock = Stock.objects.get(product=product, size=size)
        except Stock.DoesNotExist:
            raise serializers.ValidationError(f"Товар {product.name} размера {size} не найден на складе.")
        
        if stock.quantity < quantity:
            raise serializers.ValidationError(f"Недостаточно товара на складе. В наличии: {stock.quantity}")
        
        data['price'] = product.selling_price * quantity
        
        customer = data.get('customer')
        if customer and customer.role != 'customer':
            raise serializers.ValidationError({"customer": "Покупатель должен иметь роль customer."})
        if customer and not customer.is_approved:
            raise serializers.ValidationError({"customer": "Клиент не одобрен продавцом."})
        
        return data