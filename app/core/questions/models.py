from django.db import models
from django.forms import model_to_dict
from core.erp.models import Category, Dominio, Indicador, Escala
from core.user.models import Area, User
from django.utils import timezone

class Question(models.Model):
    dom = models.ForeignKey(Dominio, on_delete=models.CASCADE, verbose_name='Dominio', null=True, blank=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría', null=True, blank=True)
    ind = models.ForeignKey(Indicador, on_delete=models.CASCADE, verbose_name='Indicador', null=True, blank=True)
    question_text = models.CharField(max_length=400)

    def __str__(self):
        return self.question_text
    
    def has_user_answered(self, user):
        return self.answers.filter(user=user).exists()

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['dom'] = self.dom.toJSON()
        item['ind'] = self.ind.toJSON()
        return item 

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['id']
        
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Pregunta', related_name='answers')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='Área', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario', null=True)
    #score = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True)
    #score2 = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True)
    score = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True)
    comp = models.BooleanField(default=False, verbose_name='Enviado a Evaluación')
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha', null=True)
    escala = models.ForeignKey(Escala, on_delete=models.CASCADE, verbose_name='Escala', null=True, blank=True)


    def __str__(self):
        return f'{self.question.question_text} - {self.escala.name} - {self.score}'
    
    def toJSON(self):
        return {
            'id': self.id,
            'question': self.question.question_text,
            'area': self.area.name if self.area else None,
            'score': self.score,
            # 'score2': self.score2,
            'comp': "Enviada" if self.comp else "Sin enviar",
            'created_at': self.fecha.strftime('%Y-%m-%d') if self.fecha else None,
        }
    
    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = timezone.now().date()
        
        if self.user and not self.area:
            self.area = self.user.area
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'