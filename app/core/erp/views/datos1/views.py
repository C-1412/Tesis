from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from core.erp.mixins import ValidatePermissionRequiredMixin

from django.db.models import Count
from core.questions.models import Question, Answer
from core.user.models import User
from core.erp.models import Area, Dominio, Category
from django.contrib.auth.models import Group

from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO

class DatosAreaListView(LoginRequiredMixin, ListView):
    template_name = 'datos1/list.html'
    permission_required = 'view_answer'
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Datos'
        context['list_url'] = reverse_lazy('erp:datos_area_list')
        context['entity'] = 'Datos'

        # Obtener todas las áreas
        areas = Area.objects.all()

        # Filtrar por área seleccionada
        selected_area_id = self.request.GET.get('area')
        if selected_area_id:
            selected_area = get_object_or_404(Area, id=selected_area_id)
            areas = areas.filter(id=selected_area.id)
        else:
            selected_area = None

        # Para cada área (filtrada o todas) se obtienen las preguntas y se calculan los votos
        for area in areas:
            questions = Question.objects.filter(answers__area=area).distinct()
            for question in questions:
                # Calcular usuarios que han respondido y total de usuarios en el área
                answered_users_count = User.objects.filter(groups__name='Usuario', answer__comp=True, answer__area=area).distinct().count()
                total_users_count = User.objects.filter(groups__name='Usuario', area=area).distinct().count()
                question.answered_users_count = answered_users_count
                question.total_users_count = total_users_count

                # Calcular los votos agrupados por escala.
                # Se buscan las respuestas verificadas (comp=True) para la pregunta y el área
                answers = Answer.objects.filter(question=question, comp=True, area=area)
                votes_by_escala = {}
                for ans in answers:
                    escala_nombre = ans.escala.name if ans.escala else "Sin Escala"
                    if escala_nombre not in votes_by_escala:
                        votes_by_escala[escala_nombre] = {}
                    votes_by_escala[escala_nombre][ans.score] = votes_by_escala[escala_nombre].get(ans.score, 0) + 1
                question.votes_by_escala = votes_by_escala

            # Se adjuntan las preguntas al objeto área y se calcula un rowspan (opcional)
            area.questions = questions
            area.row_span = questions.count() + 1

        context['areas'] = Area.objects.all()      # Todas las áreas (para el select)
        context['filtered_areas'] = areas            # Áreas filtradas según la selección
        context['selected_area_id'] = selected_area_id
        return context

class DatosAreaPDFView(LoginRequiredMixin, View):
    permission_required = 'view_answer'

    def get(self, request, *args, **kwargs):
        # Obtener el ID del área seleccionada
        selected_area_id = request.GET.get('area')

        # Filtrar las áreas
        areas = Area.objects.all()
        if selected_area_id and selected_area_id != 'None':
            selected_area = get_object_or_404(Area, id=selected_area_id)
            areas = areas.filter(id=selected_area.id)
        else:
            selected_area = None

        questions = []
        for area in areas:
            area_questions = Question.objects.filter(answers__area=area).distinct()
            for question in area_questions:
                # Calcular usuarios que han respondido y total de usuarios en el área
                answered_users_count = User.objects.filter(groups__name='Usuario', answer__comp=True, answer__area=area).distinct().count()
                total_users_count = User.objects.filter(groups__name='Usuario', area=area).distinct().count()
                question.answered_users_count = answered_users_count
                question.total_users_count = total_users_count

                # Calcular votos agrupados por escala
                answers = Answer.objects.filter(question=question, comp=True, area=area)
                votes_by_escala = {}
                for ans in answers:
                    escala_nombre = ans.escala.name if ans.escala else "Sin Escala"
                    if escala_nombre not in votes_by_escala:
                        votes_by_escala[escala_nombre] = {}
                    votes_by_escala[escala_nombre][ans.score] = votes_by_escala[escala_nombre].get(ans.score, 0) + 1
                question.votes_by_escala = votes_by_escala

            questions.extend(area_questions)

        # Renderizar la plantilla para PDF
        template_path = 'datos1/list_pdf.html'
        context = {
            'title': 'Listado de Datos',
            'questions': questions,
        }
        html_string = render_to_string(template_path, context)

        # Generar PDF utilizando xhtml2pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Informe_por_Area.pdf"'
        buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html_string, dest=buffer, encoding='utf-8')
        if not pisa_status.err:
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response

        return HttpResponse('Error al generar el PDF: %s' % pisa_status.err, status=400)
