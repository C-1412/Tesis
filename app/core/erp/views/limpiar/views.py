from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.user.models import User, Area
from core.questions.models import Answer
from django.contrib.auth.models import Group
from django.contrib import messages

class LimpiarDatosView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'limpiar/list.html'
    permission_required = 'view_user'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                area_id = request.POST.get('area_id', None)

                user_group = Group.objects.get(name='Usuario')
                users = User.objects.filter(groups=user_group).all()

                if area_id:
                    users = users.filter(area_id=area_id)
                data = [{'id': u.id, 'username': u.username, 'area': u.area.name if u.area else ''} for u in users]
                
            elif action == 'delete_answers':
                user_ids = request.POST.getlist('user_ids[]')
                Answer.objects.filter(user_id__in=user_ids).delete()
                data['success'] = True
            else:
                data['error'] = 'Acción no válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['areas'] = Area.objects.all()
        return context
