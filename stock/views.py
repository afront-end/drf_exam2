from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdminOrStorekeeper
from .models import Stock
from .serializers import StockSerializer

class StockListCreateView(generics.ListCreateAPIView):
    queryset = Stock.objects.select_related('product').all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'size']
    ordering_fields = ['product__name', 'size', 'quantity']

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrStorekeeper]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()

class StockUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.select_related('product')
    serializer_class = StockSerializer
    permission_classes = [IsAdminOrStorekeeper]
    lookup_field = 'id'