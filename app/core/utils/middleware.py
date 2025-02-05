from django.contrib.auth.models import Group
from django.utils.deprecation import MiddlewareMixin
from core.erp.models import Dominio, Category

class CheckUserGroupMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            user_groups = request.user.groups.values_list('name', flat=True)
            request.session['is_administrador_group'] = 'Administrador' in user_groups
            request.session['is_moderador_group'] = 'Moderador' in user_groups
            request.session['is_gestor_group'] = 'Gestor' in user_groups
            request.session['is_usuario_group'] = 'Usuario' in user_groups
