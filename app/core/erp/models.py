from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.models import BaseModel

class Indicador(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'
        ordering = ['id']

class Escala(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Escala'
        verbose_name_plural = 'Escalas'
        ordering = ['id']

class Dominio(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    escalas = models.ManyToManyField(Escala, verbose_name='Escalas', blank=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['escalas'] = list(self.escalas.values('id', 'name'))
        return item

    class Meta:
        verbose_name = 'Dominio'
        verbose_name_plural = 'Dominios'
        ordering = ['id']

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    sec = models.CharField(max_length=150, null=True, blank=True, verbose_name='Sección')
    dom = models.ForeignKey(Dominio, on_delete=models.CASCADE, verbose_name='Dominio', null=True, blank=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['dom'] = self.dom.toJSON()
        return item

    class Meta:
        verbose_name = 'Dimensión'
        verbose_name_plural = 'Dimensiones'
        ordering = ['id']


class Area(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Area'
        ordering = ['id']
