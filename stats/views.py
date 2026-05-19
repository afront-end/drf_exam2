from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from sales.models import Sale
from products.models import Product
from stock.models import Stock
from users.permissions import IsAdminOrSeller

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]
    
    def get(self, request):
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday()) 
        month_start = today.replace(day=1)
        
        sales_today = Sale.objects.filter(created_at__date=today)
        total_sales_today = sales_today.aggregate(total=Sum('price'))['total'] or 0
        
        sales_week = Sale.objects.filter(created_at__date__gte=week_start)
        total_sales_week = sales_week.aggregate(total=Sum('price'))['total'] or 0
        
        sales_month = Sale.objects.filter(created_at__date__gte=month_start)
        total_sales_month = sales_month.aggregate(total=Sum('price'))['total'] or 0
        
        top_products = Sale.objects.values('product__name').annotate(
            sold_count=Sum('quantity')
        ).order_by('-sold_count')[:5]
        
        low_stock_items = Stock.objects.filter(quantity__lte=2).select_related('product')[:10]
        low_stock_data = [
            {"product": item.product.name, "size": item.size, "quantity": item.quantity}
            for item in low_stock_items
        ]
        
        sales_by_seller = Sale.objects.values('seller__full_name', 'seller__username').annotate(
            total=Sum('price'),
            count=Count('id')
        ).order_by('-total')[:10]
        sales_by_seller_data = [
            {"seller": item['seller__full_name'] or item['seller__username'], 
             "total": item['total'], 
             "count": item['count']}
            for item in sales_by_seller
        ]
        
        data = {
            "total_sales_today": total_sales_today,
            "total_sales_week": total_sales_week,
            "total_sales_month": total_sales_month,
            "top_products": list(top_products),
            "low_stock_items": low_stock_data,
            "sales_by_seller": sales_by_seller_data,
        }
        return Response(data)