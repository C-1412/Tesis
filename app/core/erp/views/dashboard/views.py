from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.shortcuts import redirect
from django.db.models import Count, Q

from core.questions.models import *

class AllQuestionsListView(ListView):
    model = Question
    template_name = 'dashboard.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        dominio_id = self.request.GET.get('dominio')
        categoria_id = self.request.GET.get('categoria')

        self.request.session['dominio_id'] = dominio_id
        self.request.session['categoria_id'] = categoria_id

        if dominio_id and categoria_id:
            queryset = queryset.filter(dom_id=dominio_id, cat_id=categoria_id)
        return queryset

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
        context['request_user'] = self.request.user
        context['dominios'] = Dominio.objects.all()
        context['category'] = Category.objects.all()

        questions = self.get_queryset()
        user_votes_tipo1 = {}
        user_votes_tipo2 = {}
        user = self.request.user

        #for question in questions:
        #    user_votes_tipo1[question.id] = Answer.objects.filter(question=question, score__isnull=False).values('score').annotate(count=Count('score'))
        #    user_votes_tipo2[question.id] = Answer.objects.filter(question=question, score2__isnull=False).values('score2').annotate(count=Count('score2'))

        context['user_votes_tipo1'] = user_votes_tipo1
        context['user_votes_tipo2'] = user_votes_tipo2

        # Obtener respuestas que cumplen la condición comp=True y contarlas
        answers_comp_true = Answer.objects.filter(question__in=questions, comp=True)
        answers_comp_counts = answers_comp_true.values('question').annotate(count=Count('question'))

        user_answered_questions = {question.id: question.has_user_answered(user) for question in questions}
        context['user_answered_questions'] = user_answered_questions

        context['answers_comp_counts'] = {item['question']: item['count'] for item in answers_comp_counts}

        answers = Answer.objects.filter(user=user)
        all_questions_answered = all(question.has_user_answered(user) for question in Question.objects.all())
        #answers_completed = answers.filter(comp=True).exists()
        answers_completed = answers.filter(user=user).exists() and all(answer.comp for answer in answers.filter(user=user))
        print(answers.filter(user=user).exists())
        print(all(answer.comp for answer in answers.filter(user=user)))
        # Verificar si hay alguna respuesta que no esté marcada como comp=True
        any_answer_not_comp = answers.filter(comp=False).exists()

        context['all_questions_answered'] = all_questions_answered
        context['answers_completed'] = answers_completed
        context['any_answer_not_comp'] = any_answer_not_comp

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

        # Añadir las preguntas que no están enviadas a comprobación
        # context['reopened_questions'] = [question.id for question in questions if not question.answers.filter(user=user, comp=True).exists()]

        return context
    