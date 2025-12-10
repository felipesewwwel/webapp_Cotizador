from django.db import models
from django.db.models import Sum

class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    phone = models.CharField(max_length=50, verbose_name="Teléfono")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    rut = models.CharField(max_length=20, verbose_name="RUT")

    def __str__(self):
        return self.name

class Project(models.Model):
    # Opciones estáticas para selectores
    STATUS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Finalizado', 'Finalizado'),
    ]
    PAYMENT_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Pagado', 'Pagado'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    delivery_address = models.CharField(max_length=255, verbose_name="Dirección de Entrega")
    # Cambio importante: DateField en lugar de String
    start_date = models.DateField(verbose_name="Fecha de Inicio")
    project_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendiente')
    payment_status = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='Pendiente')
    
    # Cambio importante: DecimalField para dinero
    deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Abono")
    other_windows = models.TextField(blank=True, null=True, verbose_name="Notas / Otras Ventanas")
    other_windows_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Valor Adicional")

    def __str__(self):
        return f"{self.client.name} - {self.start_date}"

    @property
    def total_cost(self):
        """Calcula: Suma precios ventanas + valor adicional"""
        windows_total = self.windows.aggregate(total=Sum('price'))['total'] or 0
        return windows_total + self.other_windows_value

class Ventana(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='windows')
    height = models.CharField(max_length=50, verbose_name="Alto")
    width = models.CharField(max_length=50, verbose_name="Ancho")
    line = models.CharField(max_length=100, verbose_name="Línea")
    color = models.CharField(max_length=50, verbose_name="Color")
    crystal = models.CharField(max_length=100, verbose_name="Cristal")
    
    # Precio numérico para cálculos
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio")
    
    material_cut = models.BooleanField(default=False, verbose_name="Corte Material")
    glass_cut = models.BooleanField(default=False, verbose_name="Corte Vidrio")

    def __str__(self):
        return f"{self.width}x{self.height} ({self.line})"