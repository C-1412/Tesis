from datetime import datetime

from django import forms
from django.forms import ModelForm

from core.erp.models import Category, Area, Dominio, Indicador, Escala
from core.questions.models import Question


class PreguntaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question_text'].widget.attrs['autofocus'] = True

    class Meta:
        model = Question
        fields = '__all__'
        labels = {
            'question_text': 'Texto de la pregunta',
            'cat': 'Dimensión'
        }
        widgets = {
            'cat': forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'dom': forms.Select(attrs={'class': 'form-control', 'style': 'width: 100%'}),
            'question_text': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese una pregunta',
                    'rows': 4,
                    'cols': 3
                },               
            ),
            'ind': forms.TextInput(attrs={'class': 'form-control autocomplete', 'placeholder': 'Buscar indicador'})

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    
class DominioForm(ModelForm):
    escalas = forms.ModelMultipleChoiceField(
        queryset=Escala.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        if self.instance.pk:
            self.fields['escalas'].initial = self.instance.escalas.all()

    def save(self, commit=True):
        dominio = super().save(commit=False)
        if commit:
            dominio.save()
            self.cleaned_data['escalas'] and dominio.escalas.set(self.cleaned_data['escalas'])
        return dominio

    class Meta:
        model = Dominio
        fields = ['name', 'escalas']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
        }

class EscalaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Escala
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            )
            ,
            'desc': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese un descripción',
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'desc': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
class AreaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Area
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class IndicadorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Indicador
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    