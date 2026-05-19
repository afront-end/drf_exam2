from rest_framework import generics, status, filters, serializers
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from .models import Sale
from .serializers import SaleSerializer, SaleCreateSerializer
from users.permissions import IsAdminOrSeller, IsCustomer, IsApprovedCustomer, IsAdmin,IsNotStorekeeper
from stock.models import Stock
from users.models import User



class SaleListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,IsNotStorekeeper]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['seller', 'payment_method']
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        queryset = Sale.objects.select_related('product', 'customer', 'seller')
        
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)
        
        if user.role == 'admin':
            return queryset
        elif user.role == 'seller':
            return queryset
        elif user.role == 'customer':
            return queryset.filter(customer=user)
        else:
            return Sale.objects.none()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SaleCreateSerializer
        return SaleSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role in ('admin', 'seller'):
            customer = serializer.validated_data.get('customer')
            if not customer:
                raise serializers.ValidationError({"customer": "Продавец должен указать клиента."})
            seller = user
        elif user.role == 'customer':
            if not user.is_approved:
                raise serializers.ValidationError("Ваш аккаунт не одобрен продавцом.")
            customer = user
            # Находим администратора для seller (или можно создать отдельного онлайн-продавца)
            admin_user = User.objects.filter(role='admin').first()
            if not admin_user:
                raise serializers.ValidationError("Системная ошибка: нет администратора.")
            seller = admin_user
        else:
            raise serializers.ValidationError("Вы не можете создавать продажи.")
        
        with transaction.atomic():
            sale = serializer.save(seller=seller, price=serializer.validated_data.get('price'))
            stock = Stock.objects.select_for_update().get(product=sale.product, size=sale.size)
            stock.quantity -= sale.quantity
            stock.save()
class SaleDetailView(generics.RetrieveAPIView):
    queryset = Sale.objects.select_related('product', 'customer', 'seller')
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Sale.objects.filter(customer=user)
        return Sale.objects.all()

class MyPurchasesView(generics.ListAPIView):
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    
    def get_queryset(self):
        return Sale.objects.filter(customer=self.request.user).select_related('product', 'seller')