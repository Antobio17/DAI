from django.contrib import admin
from .models import Libro, Prestamo, Ejemplar

# Register your models here.
admin.site.register(Libro)
admin.site.register(Prestamo)
admin.site.register(Ejemplar)