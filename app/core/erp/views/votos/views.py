from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,DetailView
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.questions.models import Question
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.questions.models import Answer
from django.db.models import Count
from django.contrib import messages


class VotosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Question
    template_name = 'votos/list.html'
    permission_required = 'view_answer'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                questions = Question.objects.filter(answers__comp=True).distinct()
                for question in questions:
                    item = question.toJSON()
                    item['comp_true'] = question.answers.filter(comp=True).count()
                    item['comp_false'] = question.answers.filter(comp=False).count()
                    data.append(item)
            elif action == 'update_comp':
                question_ids = request.POST.getlist('question_id')
                comp_values = request.POST.getlist('comp_value')
                for question_id, comp_value in zip(question_ids, comp_values):
                    comp_value = comp_value == 'true'
                    Answer.objects.filter(question_id=question_id).update(comp=comp_value)#.delete()    #
                data['success'] = 'Comprobación actualizada'
                messages.success(request, "Comprobación actualizada correctamente")
            else:
                data['error'] = 'Acción no válida'
                messages.error(request,'Acción no válida')
        except Exception as e:
            data['error'] = str(e)
            messages.success(request, e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Votos'
        context['list_url'] = reverse_lazy('erp:votos_list')
        context['entity'] = 'Votos'
        return context

