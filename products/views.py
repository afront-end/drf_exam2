from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAdmin, IsAdminOrStorekeeper
from .models import Product
from .serializers import ProductSerializer, ProductCreateUpdateSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.prefetch_related('stocks').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrStorekeeper]
        return super().get_permissions()

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.prefetch_related('stocks')
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = [IsAdmin]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [IsAdminOrStorekeeper]
        else: 
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()