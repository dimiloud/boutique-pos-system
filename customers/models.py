from django.db import models
from django.core.validators import MinValueValidator, EmailValidator

class Customer(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Prénom')
    last_name = models.CharField(max_length=100, verbose_name='Nom')
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        validators=[EmailValidator()]
    )
    phone = models.CharField(max_length=20, verbose_name='Téléphone')
    address = models.TextField(blank=True, verbose_name='Adresse')
    loyalty_points = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Points de fidélité'
    )
    active = models.BooleanField(default=True, verbose_name='Actif')
    notes = models.TextField(blank=True, verbose_name='Notes')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modifié le')

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def loyalty_euros(self):
        return self.loyalty_points / 100  # 100 points = 1€