from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import PreguntaForm
from core.erp.mixins import ValidatePermissionRequiredMixin

from core.questions.models import *

class PreguntaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Question
    template_name = 'pregunta/list.html'
    permission_required = 'view_question'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Question.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Preguntas'
        context['create_url'] = reverse_lazy('erp:pregunta_create')
        context['list_url'] = reverse_lazy('erp:pregunta_list')
        context['entity'] = 'Preguntas'
        return context
        

class PreguntaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Question
    form_class = PreguntaForm
    template_name = 'pregunta/create.html'
    success_url = reverse_lazy('erp:pregunta_list')
    permission_required = 'add_question'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
                Answer.objects.all().update(comp=False)              
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación una Pregunta'
        context['entity'] = 'Preguntas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class PreguntaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Question
    form_class = PreguntaForm
    template_name = 'pregunta/create.html'
    success_url = reverse_lazy('erp:pregunta_list')
    permission_required = 'change_question'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Pregunta'
        context['entity'] = 'Preguntas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class PreguntaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Question
    template_name = 'pregunta/delete.html'
    success_url = reverse_lazy('erp:pregunta_list')
    permission_required = 'delete_question'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Pregunta'
        context['entity'] = 'Preguntas'
        context['list_url'] = self.success_url
        return context

from django.views.generic import View
class IndicadorAutocomplete(View):
    def get(self, request, *args, **kwargs):
        if 'term' in request.GET:
            term = request.GET.get('term')
            indicadores = Indicador.objects.filter(name__icontains=term)
            data = [{'id': indicador.id, 'value': indicador.name} for indicador in indicadores]
            return JsonResponse(data, safe=False)
        return JsonResponse([], safe=False)