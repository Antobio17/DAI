from django.db import models
from django.utils import timezone
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
import datetime


# Create your models here.
class Libro(models.Model):
    titulo = models.CharField(max_length=200, primary_key=True)
    autor = models.CharField(max_length=200)
    portada = models.FileField(upload_to='static/img', blank=True)
    resumen = models.TextField(max_length=1000, help_text="Breve resumen del libro")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    precio = models.FloatField(null=True) 

    def __str__(self):
        return self.titulo
    def get_absolute_url(self):
        return reverse('libro-detail', kwargs={'pk': self.pk})


class Ejemplar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para el ejemplar del libro físico")
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True) 
    #datetime.date.today()+datetime.timedelta(days=7)
    ESTADO_PRESTAMO = (
        ('p', 'Prestado'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    estado = models.CharField(max_length=1, choices=ESTADO_PRESTAMO, blank=True, default='d', help_text='Disponibilidad del libro')
        
    def __str__(self):
        return '%s (%s)' % (self.id,self.libro.titulo)

    def get_absolute_url(self):
        return reverse('libro-detail', kwargs={'pk': self.libro.pk})


class Prestamo(models.Model):
    ejemplar = models.ForeignKey(Ejemplar, primary_key=True, on_delete=models.CASCADE)
    prestatario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    devolucion = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.ejemplar.__str__() + ' prestado a ' +  self.prestatario.__str__()
    
    @property
    def expirado(self):
        if self.devolucion and datetime.date.today() > self.devolucion:
            return True
        return False