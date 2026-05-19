from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks', verbose_name='Товар')
    size = models.IntegerField(
        validators=[MinValueValidator(35), MaxValueValidator(42)],
        verbose_name='Размер обуви'
    )
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Количество на складе'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Остаток'
        verbose_name_plural = 'Остатки'
        unique_together = ['product', 'size']
        ordering = ['product__name', 'size']

    def __str__(self):
        return f"{self.product.name} - размер {self.size}: {self.quantity} шт."