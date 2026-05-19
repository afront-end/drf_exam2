from django.urls import path
from .views import SaleListCreateView, SaleDetailView, MyPurchasesView

urlpatterns = [
    path('', SaleListCreateView.as_view(), name='sales'),
    path('my/', MyPurchasesView.as_view(), name='my-purchases'),
    path('<int:id>/', SaleDetailView.as_view(), name='sale-detail'),
]