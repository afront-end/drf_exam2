from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название товара')
    description = models.TextField(blank=True, verbose_name='Описание')
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Цена закупки'
    )
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Цена продажи'
    )
    photo = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Фото')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_products', verbose_name='Добавил')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name