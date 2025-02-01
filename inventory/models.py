from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nom')
    description = models.TextField(blank=True, verbose_name='Description')

    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]

    name = models.CharField(max_length=200, verbose_name='Nom')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Catégorie')
    description = models.TextField(blank=True, verbose_name='Description')
    sku = models.CharField(max_length=50, unique=True, verbose_name='SKU')
    barcode = models.CharField(max_length=13, unique=True, verbose_name='Code-barres')
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, verbose_name='Taille')
    color = models.CharField(max_length=50, verbose_name='Couleur')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Prix de vente'
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Prix d\'achat'
    )
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Quantité en stock'
    )
    alert_quantity = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1)],
        verbose_name='Quantité d\'alerte'
    )
    active = models.BooleanField(default=True, verbose_name='Actif')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modifié le')

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.size}, {self.color})'

    @property
    def low_stock(self):
        return self.stock_quantity <= self.alert_quantity

    @property
    def margin(self):
        return self.price - self.cost_price