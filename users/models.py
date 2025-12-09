from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado con campos adicionales
    """
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('STAFF', 'Staff'),
        ('CLIENTE', 'Cliente'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='CLIENTE'
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} - {self.password}"