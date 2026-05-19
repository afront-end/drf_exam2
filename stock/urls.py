from django.urls import path
from .views import StockListCreateView, StockUpdateView

urlpatterns = [
    path('', StockListCreateView.as_view(), name='stock-list-create'),
    path('<int:id>/', StockUpdateView.as_view(), name='stock-update'),
]