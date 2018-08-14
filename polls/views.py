# from django.shortcuts import render
from django.utils import timezone
# Create your views here.
from django.http import HttpResponseRedirect
from .models import Choice, Question
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You did not select a choice!",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    # return HttpResponse("You are voting on question %s." % question_id)
    return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))