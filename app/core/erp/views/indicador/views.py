from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import IndicadorForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Indicador

class IndicadorListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Indicador
    template_name = 'indicador/list.html'
    permission_required = 'view_indicador'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Indicador.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Indicadores'
        context['create_url'] = reverse_lazy('erp:indicador_create')
        context['list_url'] = reverse_lazy('erp:indicador_list')
        context['entity'] = 'Indicador'
        return context


class IndicadorCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Indicador
    form_class = IndicadorForm
    template_name = 'indicador/create.html'
    success_url = reverse_lazy('erp:indicador_list')
    permission_required = 'add_indicador'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        data = {}
        try:
            action = request.POST['action']
            print(action)
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un Indicador'
        context['entity'] = 'Indicadores'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class IndicadorUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Indicador
    form_class = IndicadorForm
    template_name = 'indicador/create.html'
    success_url = reverse_lazy('erp:indicador_list')
    permission_required = 'change_indicador'
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
        context['title'] = 'Edición un Indicador'
        context['entity'] = 'Indicadores'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class IndicadorDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Indicador
    template_name = 'indicador/delete.html'
    success_url = reverse_lazy('erp:indicador_list')
    permission_required = 'delete_indicador'
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
        context['title'] = 'Eliminación de un Indicador'
        context['entity'] = 'Indicadores'
        context['list_url'] = self.success_url
        return context
