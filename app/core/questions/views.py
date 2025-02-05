from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from core.erp.mixins import ValidatePermissionRequiredMixin
from core.questions.models import Question, Answer
from core.erp.models import Dominio, Category

class QuestionsListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Question
    template_name = 'questions/index.html'
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
                position = 1
                for i in Question.objects.all():
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
        context['title'] = 'Listado de Preguntas'
        context['entity'] = 'Preguntas'

        user = self.request.user
        answers = Answer.objects.filter(user=user)
        all_questions_answered = all(question.has_user_answered(user) for question in Question.objects.all())
        answers_completed = answers.filter(comp=True).exists()
        
        context['all_questions_answered'] = all_questions_answered
        context['answers_completed'] = answers_completed

        # Para el listado, se puede armar un diccionario con la pregunta y si fue contestada en alguna escala.
        user_answered_questions = {}
        for question in Question.objects.all():
            user_answered_questions[question.id] = question.answers.filter(user=user).exists()
        context['user_answered_questions'] = user_answered_questions

        return context

    def all_questions_answered(self):
        user = self.request.user
        total_questions = Question.objects.count()
        answered_questions = Answer.objects.filter(user=user).count()
        
        return total_questions == answered_questions

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'questions/detail.html'

    def post(self, request, *args, **kwargs):
        question = self.get_object()
        user = request.user
        # Obtenemos las escalas asociadas al dominio de la pregunta
        escalas = question.dom.escalas.all()
        error_flag = False

        # Verificar que se haya enviado un valor para cada escala
        for escala in escalas:
            if not request.POST.get(f"score_{escala.id}"):
                messages.error(request, f"El valor para la escala {escala.name} es obligatorio.")
                error_flag = True

        if error_flag:
            return self.get(request, *args, **kwargs)

        area = user.area if hasattr(user, 'area') else None
        # Para cada escala, guardamos o actualizamos la respuesta
        for escala in escalas:
            score = request.POST.get(f"score_{escala.id}")
            Answer.objects.update_or_create(
                question=question,
                user=user,
                escala=escala,
                defaults={'score': score, 'area': area}
            )

        dominio_id = request.session.get('dominio_id', '')
        categoria_id = request.session.get('categoria_id', '')
        if dominio_id and categoria_id:
            redirect_url = reverse('erp:dashboard') + f'?dominio={dominio_id}&categoria={categoria_id}'
        else:
            redirect_url = reverse('erp:dashboard')
        return HttpResponseRedirect(redirect_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Respuestas'
        context['entity'] = 'Respuestas'
        context['dominios'] = Dominio.objects.all()
        context['category'] = Category.objects.all()
        context['error_message'] = "Ya has respondido esta pregunta."
        context['success_message'] = "Respuesta registrada con éxito."

        user = self.request.user
        question = self.get_object()
        escalas = question.dom.escalas.all()

        # Construimos un diccionario con los puntajes previos (clave: id de escala, valor: score)
        previous_scores = {}
        for escala in escalas:
            try:
                answer = Answer.objects.get(question=question, user=user, escala=escala)
                previous_scores[escala.id] = answer.score
            except Answer.DoesNotExist:
                previous_scores[escala.id] = None

        context['previous_scores'] = previous_scores
        context['escalas'] = escalas

        section_counts = {}
        for categoria in context['category']:
            questions = Question.objects.filter(cat=categoria)
            answered_count = questions.filter(answers__user=self.request.user).distinct().count()
            total_count = questions.count()
            section_counts[categoria.id] = {
                'answered_count': answered_count,
                'total_count': total_count,
            }
        context['section_counts'] = section_counts

        return context
    
class MarkAnswersCompleteView(LoginRequiredMixin, View):
    model = Answer
    template_name = 'questions/completadas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
    
        answers = Answer.objects.filter(user=user)
        all_questions_answered = all(question.has_user_answered(user) for question in Question.objects.all())
        answers_completed = answers.filter(comp=True).exists()
        
        context['all_questions_answered'] = all_questions_answered
        context['answers_completed'] = answers_completed
        
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        
        answers = Answer.objects.filter(user=user)

        all_questions_answered = all(question.has_user_answered(user) for question in Question.objects.all())
                
        if not all_questions_answered:
            messages.error(request, "Aún no has respondido todas las preguntas o no has votado en todas las respuestas.")
            return redirect('erp:dashboard')
                
        if all(answer.comp for answer in answers):
            messages.warning(request, "Ya se han enviado las respuestas.")
        else:
            answers.update(comp=True)
            messages.success(request, "Todas tus respuestas han sido marcadas como completadas.")

        return redirect('erp:dashboard')