from django.db import models
from django.core.validators import MinValueValidator
from customers.models import Customer
from inventory.models import Product

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('CASH', 'Espèces'),
        ('CARD', 'Carte bancaire'),
        ('TRANSFER', 'Virement'),
    ]

    customer = models.ForeignKey(
        Customer,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Client'
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date de vente')
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        verbose_name='Méthode de paiement'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Sous-total'
    )
    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='TVA'
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Total'
    )
    notes = models.TextField(blank=True, verbose_name='Notes')

    class Meta:
        verbose_name = 'Vente'
        verbose_name_plural = 'Ventes'
        ordering = ['-date']

    def __str__(self):
        return f'Vente #{self.id} - {self.date}'

class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Vente'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Produit'
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantité'
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Prix unitaire'
    )
    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Remise'
    )

    class Meta:
        verbose_name = 'Ligne de vente'
        verbose_name_plural = 'Lignes de vente'

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

    @property
    def total(self):
        return (self.unit_price * self.quantity) - self.discount