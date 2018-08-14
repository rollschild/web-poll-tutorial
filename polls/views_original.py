# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list
    }
    # return HttpResponse("Hello. You're at the polls index.<br/>"
    # + template.render(context, request))
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    '''
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question %s does not exist!" % question_id)
    # return HttpResponse("Here's question %s." % question_id)
    return render(request, 'polls/detail.html', {'question': question})
    '''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


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
