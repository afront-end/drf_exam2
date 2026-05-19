from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Создаёт тестовых пользователей: admin, seller, storekeeper, одобренный customer'

    def handle(self, *args, **options):
        # Создаём администратора
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'full_name': 'Администратор',
                'phone': '+992000000001',
                'role': 'admin',
                'is_approved': True,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Администратор создан (login: admin, pass: admin123)'))
        else:
            self.stdout.write('Администратор уже существует')

        # Продавец Алия
        seller, created = User.objects.get_or_create(
            username='seller1',
            defaults={
                'full_name': 'Алия',
                'phone': '+992000000002',
                'role': 'seller',
                'is_approved': True
            }
        )
        if created:
            seller.set_password('seller123')
            seller.save()
            self.stdout.write(self.style.SUCCESS('Продавец создан (login: seller1, pass: seller123)'))

        # Кладовщик Рустам
        keeper, created = User.objects.get_or_create(
            username='keeper1',
            defaults={
                'full_name': 'Рустам',
                'phone': '+992000000003',
                'role': 'storekeeper',
                'is_approved': True
            }
        )
        if created:
            keeper.set_password('keeper123')
            keeper.save()
            self.stdout.write(self.style.SUCCESS('Кладовщик создан (login: keeper1, pass: keeper123)'))

        # Одобренный клиент Малика
        customer, created = User.objects.get_or_create(
            username='customer1',
            defaults={
                'full_name': 'Малика Рахимова',
                'phone': '+992901234567',
                'role': 'customer',
                'is_approved': True
            }
        )
        if created:
            customer.set_password('customer123')
            customer.save()
            self.stdout.write(self.style.SUCCESS('Одобренный клиент создан (login: customer1, pass: customer123)'))