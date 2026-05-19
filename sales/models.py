from django.db import models
from django.core.validators import MinValueValidator
from users.models import User
from products.models import Product

class Sale(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('transfer', 'Перевод'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='sales', verbose_name='Товар')
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='purchases', verbose_name='Покупатель', limit_choices_to={'role': 'customer'})
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales_made', verbose_name='Продавец')
    size = models.IntegerField(verbose_name='Размер обуви')
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продажи')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name='Способ оплаты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время продажи')

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
        ordering = ['-created_at']

    def __str__(self):
        return f"Продажа {self.product.name} - {self.quantity} шт. - {self.price} сом."