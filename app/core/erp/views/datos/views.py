from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO

from core.erp.mixins import ValidatePermissionRequiredMixin
from core.questions.models import Question, Answer
from core.user.models import User
from core.erp.models import Category, Dominio, Area

from xhtml2pdf import pisa


class DatosListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    template_name = 'datos/list.html'
    permission_required = 'view_answer'
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Datos'
        context['list_url'] = reverse_lazy('erp:datos_list')
        context['entity'] = 'Datos'

        context['areas'] = Area.objects.all()
        context['dominios'] = Dominio.objects.all()

        # Obtener el dominio seleccionado (si lo hay)
        dominio_id = self.request.GET.get('dominio')
        if dominio_id:
            dominio = Dominio.objects.filter(id=dominio_id).first()
        else:
            dominio = None
        context['dominio'] = dominio

        # Filtrar las dimensiones según el dominio seleccionado
        if dominio_id:
            context['dimensions'] = Category.objects.filter(dom_id=dominio_id)
        else:
            context['dimensions'] = Category.objects.all()

        # Parámetro para filtrar por dimensión
        dimension_id = self.request.GET.get('dimension')

        # Filtrar las preguntas según los parámetros
        questions = Question.objects.all()
        if dimension_id:
            questions = questions.filter(cat_id=dimension_id)
        if dominio_id:
            questions = questions.filter(dom_id=dominio_id)

        # Obtener datos de usuarios del grupo "Usuario"
        user_group = Group.objects.get(name='Usuario')
        users_in_group = User.objects.filter(groups=user_group).count()
        users_with_answers_comp = User.objects.filter(groups=user_group, answer__comp=True).distinct().count()

        for question in questions:
            question.answered_users_count = users_with_answers_comp
            question.total_users_count = users_in_group

            # Agrupar las respuestas verificadas por escala y contar los votos (score)
            escala_votes = {}
            answers = Answer.objects.filter(question=question, comp=True)
            for ans in answers:
                if ans.escala:
                    key = ans.escala.id
                    if key not in escala_votes:
                        escala_votes[key] = {
                            'escala': ans.escala.name,
                            'votes': {}
                        }
                    score = ans.score
                    escala_votes[key]['votes'][score] = escala_votes[key]['votes'].get(score, 0) + 1
            question.escala_votes = escala_votes

        context['questions'] = questions
        return context


class DatosPDFView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'view_answer'

    def get(self, request, *args, **kwargs):
        # Obtener el dominio y la dimensión seleccionados vía GET
        dominio_id = request.GET.get('dominio')
        dimension_id = request.GET.get('dimension')

        # Filtrar las preguntas según los parámetros
        questions = Question.objects.all()
        if dimension_id:
            questions = questions.filter(cat_id=dimension_id)
        if dominio_id:
            questions = questions.filter(dom_id=dominio_id)

        user_group = Group.objects.get(name='Usuario')
        users_in_group = User.objects.filter(groups=user_group).count()

        for question in questions:
            answered_users_count = Answer.objects.filter(
                question=question, comp=True
            ).values('user').distinct().count()
            question.answered_users_count = answered_users_count
            question.total_users_count = users_in_group

            escala_votes = {}
            answers = Answer.objects.filter(question=question, comp=True)
            for ans in answers:
                if ans.escala:
                    key = ans.escala.id
                    if key not in escala_votes:
                        escala_votes[key] = {
                            'escala': ans.escala.name,
                            'votes': {}
                        }
                    score = ans.score
                    escala_votes[key]['votes'][score] = escala_votes[key]['votes'].get(score, 0) + 1
            question.escala_votes = escala_votes

        # Renderizar la plantilla PDF a un string
        template_path = 'datos/list_pdf.html'
        context = {
            'title': 'Listado de Datos',
            'questions': questions,
            'dimensions': Category.objects.all(),
            'dominios': Dominio.objects.all(),
        }
        html_string = render_to_string(template_path, context)

        # Generar el PDF usando xhtml2pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Informe.pdf"'
        buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html_string, dest=buffer, encoding='utf-8')

        if not pisa_status.err:
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response

        return HttpResponse('Hubo un error al generar el PDF: %s' % pisa_status.err, status=400)
