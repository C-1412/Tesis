from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO

from core.erp.mixins import ValidatePermissionRequiredMixin
from core.questions.models import Question, Answer, Indicador
from core.erp.models import Category, Dominio, Area

from xhtml2pdf import pisa

from django.db.models import Avg

class DatosMatrizView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'datos2/list.html'
    permission_required = 'view_answer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Matriz de Escalas'

        # Cargar todos los dominios para la selección
        dominios = Dominio.objects.all()
        context['dominios'] = dominios

        # Recuperar los parámetros enviados por GET
        dominio_id   = self.request.GET.get('dominio', '')
        escala1_id   = self.request.GET.get('escala1', '')
        escala2_id   = self.request.GET.get('escala2', '')
        dimension_id = self.request.GET.get('dimension', '')
        pregunta_id  = self.request.GET.get('pregunta', '')

        context['selected_dominio']   = dominio_id
        context['selected_escala1']   = escala1_id
        context['selected_escala2']   = escala2_id
        context['selected_dimension'] = dimension_id
        context['selected_pregunta']  = pregunta_id

        # Si se seleccionó un dominio, obtener sus escalas
        dominio = Dominio.objects.filter(id=dominio_id).first() if dominio_id else None
        if dominio:
            escalas = dominio.escalas.all()
        else:
            escalas = []
        context['escalas'] = escalas

        # Filtrar las dimensiones en función del dominio
        if dominio:
            dimensions = Category.objects.filter(dom=dominio)
        else:
            dimensions = Category.objects.all()
        context['dimensions'] = dimensions

        # Filtrar las preguntas según la dimensión (si se seleccionó)
        if dimension_id:
            questions = Question.objects.filter(cat__id=dimension_id)
        else:
            questions = []
        context['questions'] = questions

        # Calcular promedios y determinar cuadrante si se seleccionaron ambas escalas
        promedio1 = promedio2 = None
        cuadrante = None
        if escala1_id and escala2_id:
            answers_filter = {}
            if dominio:
                answers_filter['question__dom'] = dominio
            if dimension_id:
                answers_filter['question__cat__id'] = dimension_id
            if pregunta_id:
                answers_filter['question__id'] = pregunta_id

            answers_escala1 = Answer.objects.filter(escala__id=escala1_id, comp=True, **answers_filter)
            promedio1 = answers_escala1.aggregate(avg=Avg('score'))['avg']

            answers_escala2 = Answer.objects.filter(escala__id=escala2_id, comp=True, **answers_filter)
            promedio2 = answers_escala2.aggregate(avg=Avg('score'))['avg']

            if promedio1 is not None and promedio2 is not None:
                x_superior = promedio1 > 3
                y_superior = promedio2 > 3

                if x_superior and y_superior:
                    cuadrante = 1
                elif (not x_superior) and y_superior:
                    cuadrante = 2
                elif (not x_superior) and (not y_superior):
                    cuadrante = 3
                elif x_superior and (not y_superior):
                    cuadrante = 4

        context['promedio1'] = promedio1
        context['promedio2'] = promedio2
        context['cuadrante'] = cuadrante

        # Obtener el indicador asociado a la pregunta
        indicador = None
        if pregunta_id:
            question_obj = Question.objects.filter(id=pregunta_id).first()
            if question_obj and question_obj.ind:
                indicador = question_obj.ind
        context['indicador'] = indicador

        # Obtener el objeto de la dimensión seleccionada para mostrarlo en la matriz
        dimension_marker = None
        if dimension_id:
            dimension_marker = Category.objects.filter(id=dimension_id).first()
        context['dimension_marker'] = dimension_marker

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class DatosMatrizPDFView(LoginRequiredMixin, ValidatePermissionRequiredMixin, View):
    permission_required = 'view_answer'

    def get(self, request, *args, **kwargs):
        dominio_id   = request.GET.get('dominio', '')
        escala1_id   = request.GET.get('escala1', '')
        escala2_id   = request.GET.get('escala2', '')
        dimension_id = request.GET.get('dimension', '')
        pregunta_id  = request.GET.get('pregunta', '')

        dominio = Dominio.objects.filter(id=dominio_id).first() if dominio_id else None
        escalas = dominio.escalas.all() if dominio else []
        dimensions = Category.objects.filter(dom=dominio) if dominio else Category.objects.all()
        questions = Question.objects.filter(cat__id=dimension_id) if dimension_id else []

        promedio1 = promedio2 = None
        cuadrante = None
        if escala1_id and escala2_id:
            answers_filter = {}
            if dominio:
                answers_filter['question__dom'] = dominio
            if dimension_id:
                answers_filter['question__cat__id'] = dimension_id
            if pregunta_id:
                answers_filter['question__id'] = pregunta_id

            answers_escala1 = Answer.objects.filter(escala__id=escala1_id, comp=True, **answers_filter)
            promedio1 = answers_escala1.aggregate(avg=Avg('score'))['avg']

            answers_escala2 = Answer.objects.filter(escala__id=escala2_id, comp=True, **answers_filter)
            promedio2 = answers_escala2.aggregate(avg=Avg('score'))['avg']

            if promedio1 is not None and promedio2 is not None:
                x_superior = promedio1 > 3
                y_superior = promedio2 > 3
                if x_superior and y_superior:
                    cuadrante = 1
                elif (not x_superior) and y_superior:
                    cuadrante = 2
                elif (not x_superior) and (not y_superior):
                    cuadrante = 3
                elif x_superior and (not y_superior):
                    cuadrante = 4

        indicador = None
        if pregunta_id:
            question_obj = Question.objects.filter(id=pregunta_id).first()
            if question_obj and question_obj.ind:
                indicador = question_obj.ind

        # Obtener el objeto de la dimensión seleccionada
        dimension_marker = None
        if dimension_id:
            dimension_marker = Category.objects.filter(id=dimension_id).first()

        context = {
            'title': 'Matriz de Escalas - Informe PDF',
            'dominios': Dominio.objects.all(),
            'selected_dominio': dominio_id,
            'selected_escala1': escala1_id,
            'selected_escala2': escala2_id,
            'selected_dimension': dimension_id,
            'selected_pregunta': pregunta_id,
            'escalas': escalas,
            'dimensions': dimensions,
            'questions': questions,
            'promedio1': promedio1,
            'promedio2': promedio2,
            'cuadrante': cuadrante,
            'indicador': indicador,
            'dimension_marker': dimension_marker,
        }

        template_path = 'datos2/list_pdf.html'
        html_string = render_to_string(template_path, context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Matriz_Informe.pdf"'
        buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html_string, dest=buffer, encoding='utf-8')
        if not pisa_status.err:
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response
        return HttpResponse('Error al generar el PDF: %s' % pisa_status.err, status=400)
