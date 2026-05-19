from django.core.management.base import BaseCommand
from products.models import Product
from stock.models import Stock
from users.models import User

class Command(BaseCommand):
    help = 'Загружает тестовые товары и остатки'

    def handle(self, *args, **options):
        # Получаем кладовщика
        keeper = User.objects.filter(role='storekeeper').first()
        if not keeper:
            self.stdout.write(self.style.ERROR('Кладовщик не найден. Сначала выполните create_test_users'))
            return

        products_data = [
            {'name': 'Nike Air Max 270', 'description': 'Женские кроссовки, легкие и удобные', 
             'purchase_price': 45.00, 'selling_price': 120.00},
            {'name': 'Adidas Superstar', 'description': 'Классические кеды', 
             'purchase_price': 38.00, 'selling_price': 95.00},
            {'name': 'Ботинки зимние', 'description': 'Тёплые женские ботинки', 
             'purchase_price': 60.00, 'selling_price': 150.00},
        ]

        for data in products_data:
            product, created = Product.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'purchase_price': data['purchase_price'],
                    'selling_price': data['selling_price'],
                    'added_by': keeper
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Товар "{product.name}" добавлен'))
                # Создаём остатки для размеров 36, 37, 38, 39
                for size in [36, 37, 38, 39]:
                    Stock.objects.get_or_create(product=product, size=size, defaults={'quantity': 10})
            else:
                self.stdout.write(f'Товар "{product.name}" уже существует')