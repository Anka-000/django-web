#from django.db import models

# Create your models here.
#class area(models.Model):
#    area_id = models.AutoField(primary_key=True)
#    area_nombre = models.CharField(max_length=200)
#    area_descripcion = models.TextField()

#    def __str__(self):
#        return self.area_nombre

from django.db import models
import os

class Area(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Área")
    descripcion = models.TextField(blank=True, verbose_name="Descripción (Opcional)")
    slug = models.SlugField(unique=True, verbose_name="Identificador URL (automático)")

    class Meta:
        verbose_name = "Área / Departamento"
        verbose_name_plural = "Áreas / Departamentos"

    def __str__(self):
        return self.nombre

class TipoDocumento(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='tipos_documento', verbose_name="Pertenece al Área")
    nombre = models.CharField(max_length=200, verbose_name="Tipo de Documento (Ej. Nómina, Facturas)")
    slug = models.SlugField(verbose_name="Identificador URL")

    class Meta:
        verbose_name = "Categoría de Documento"
        verbose_name_plural = "Categorías de Documentos"
        unique_together = ('area', 'slug') # Evita duplicados en la misma área

    def __str__(self):
        return f"{self.nombre} - ({self.area.nombre})"

class Documento(models.Model):
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, related_name='documentos', verbose_name="Tipo de Documento")
    titulo = models.CharField(max_length=255, verbose_name="Título del Documento")
    fecha_publicacion = models.DateField(verbose_name="Fecha de Publicación")
    archivo_pdf = models.FileField(upload_to='documentos/%Y/%m/', verbose_name="Archivo PDF")
    
    # Campo opcional para ordenar manualmente si dos tienen la misma fecha
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Documento PDF"
        verbose_name_plural = "Documentos PDF"
        # Esto asegura que siempre se muestren del más reciente al más antiguo automáticamente
        ordering = ['-fecha_publicacion', '-created_at']

    def __str__(self):
        return f"{self.titulo} ({self.fecha_publicacion})"