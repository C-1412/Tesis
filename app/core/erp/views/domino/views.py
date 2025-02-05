from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import DominioForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Dominio

class DominioListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Dominio
    template_name = 'dominio/list.html'
    permission_required = 'view_dominio'

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
                for i in Dominio.objects.all():
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
        context['title'] = 'Listado de Dominios'
        context['create_url'] = reverse_lazy('erp:dominio_create')
        context['list_url'] = reverse_lazy('erp:dominio_list')
        context['entity'] = 'Dominio'
        return context


class DominioCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Dominio
    form_class = DominioForm
    template_name = 'dominio/create.html'
    success_url = reverse_lazy('erp:dominio_list')
    permission_required = 'add_dominio'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                instance = form.save(commit=False)
                instance.save()
                form.save_m2m()
                data = instance.toJSON()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un Dominio'
        context['entity'] = 'Dominios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class DominioUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Dominio
    form_class = DominioForm
    template_name = 'dominio/create.html'
    success_url = reverse_lazy('erp:dominio_list')
    permission_required = 'change_dominio'
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
                instance = form.save(commit=False)
                instance.save()
                form.save_m2m()
                data = instance.toJSON()
                
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Dominio'
        context['entity'] = 'Dominios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class DominioDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Dominio
    template_name = 'dominio/delete.html'
    success_url = reverse_lazy('erp:dominio_list')
    permission_required = 'delete_dominio'
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
        context['title'] = 'Eliminación de un Dominio'
        context['entity'] = 'Dominios'
        context['list_url'] = self.success_url
        return context
