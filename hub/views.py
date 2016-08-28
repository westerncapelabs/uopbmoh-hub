from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.defaulttags import register
from django.core.context_processors import csrf
from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# from django.utils import timezone
import dateutil.parser

from .models import FacilityCode
from .services import ContinuousLearningApiClient, IdentityStoreApiClient
from .forms import (QuestionForm, QuizForm, QuizAddQuestionsForm,
                    IdentitiesFilterForm)
from .serializers import FacilityCodeSerializer


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_date(date_string):
    if date_string is not None:
        return dateutil.parser.parse(date_string)

clApi = ContinuousLearningApiClient(
    api_url=settings.CONTINUOUS_LEARNING_URL,
    auth_token=settings.CONTINUOUS_LEARNING_TOKEN
)

idApi = IdentityStoreApiClient(
    api_url=settings.IDENTITY_STORE_URL,
    auth_token=settings.IDENTITY_STORE_TOKEN
)


class FacilityCodeViewSet(viewsets.ModelViewSet):
    """ API endpoint that allows facility codes to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    queryset = FacilityCode.objects.all()
    serializer_class = FacilityCodeSerializer


@login_required(login_url='/login/')
def index(request):
    context = {
        "stats": {}
    }
    stats = clApi.get_stats()
    context.update({
        "stats": stats
    })
    context.update(csrf(request))
    return render_to_response("hub/index.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def quiz_results(request):

    context = {
        "quizzes": {}
    }
    quizzes = clApi.get_quizzes()
    for quiz in quizzes["results"]:
        context["quizzes"].update({quiz["id"]: quiz["description"]})
    results = clApi.get_trackers()
    context.update({
        "results": results
    })
    context.update(csrf(request))
    return render_to_response("hub/quiz-results.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def quiz_results_detail(request, tracker_id):

    context = {
        "quizzes": {}
    }
    quizzes = clApi.get_quizzes()
    for quiz in quizzes["results"]:
        context["quizzes"].update({quiz["id"]: quiz["description"]})
    result = clApi.get_tracker(tracker_id)
    answers = clApi.get_answers(params={"tracker": tracker_id})
    identity = idApi.get_identity(result["identity"])
    context.update({
        "result": result,
        "answers": answers,
        "identity": identity
    })
    context.update(csrf(request))
    return render_to_response("hub/quiz-results-detail.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def quizzes(request):

    context = {}
    quizzes = clApi.get_quizzes({"archived": False})
    context.update({
        "quizzes": quizzes
    })
    context.update(csrf(request))
    return render_to_response("hub/quizzes.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def results_download(request):
    results = clApi.results_download()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    response.write(results.text)
    return response


@login_required(login_url='/login/')
def quiz_detail(request, quiz_id):

    context = {}
    quiz = clApi.get_quiz(quiz_id)
    questions = []
    for question in quiz["questions"]:
        questions.append(clApi.get_question(question))
    context.update({
        "quiz": quiz,
        "questions": questions
    })
    context.update(csrf(request))
    return render_to_response("hub/quiz-detail.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def quiz_edit(request, quiz_id):
    context = {}
    questions = []
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            data = {
                "description": form.cleaned_data['description'],
                "active": form.cleaned_data['active'],
                "archived": form.cleaned_data['archived']
            }
            if quiz_id == "new":
                quiz = clApi.create_quiz(data)
            else:
                quiz = clApi.update_quiz(quiz_id, data)
            return redirect('quiz-detail', quiz_id=quiz["id"])
    else:
        form = QuizForm()
        if quiz_id != "new":
            quiz = clApi.get_quiz(quiz_id)
            questions = clApi.get_questions(params={"quiz": quiz_id})
            form.fields["description"].initial = quiz["description"]
            form.fields["active"].initial = quiz["active"]
            form.fields["archived"].initial = quiz["archived"]

    context.update({
        "questions": questions,
        "form": form
    })
    context.update(csrf(request))
    return render_to_response("hub/quiz-edit.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def quiz_add_questions(request, quiz_id):
    context = {}
    quiz = clApi.get_quiz(quiz_id)
    questions = clApi.get_questions(params={"active": True})
    if request.method == "POST":
        form = QuizAddQuestionsForm(request.POST)
        form.full_clean()
        lists = dict(form.data.lists())
        if "questions" in lists:
            quiz["questions"] = quiz["questions"] + lists["questions"]
            quiz = clApi.update_quiz(quiz_id, quiz)
        return redirect('quiz-detail', quiz_id=quiz["id"])

    context.update({
        "quiz": quiz,
        "questions": questions
    })
    context.update(csrf(request))
    return render_to_response("hub/quiz-add-questions.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def questions(request):

    context = {}
    questions = clApi.get_questions()
    context.update({
        "questions": questions
    })
    context.update(csrf(request))
    return render_to_response("hub/questions.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def question_detail(request, question_id):
    context = {}
    question = clApi.get_question(question_id)
    context.update({
        "question": question
    })
    context.update(csrf(request))
    return render_to_response("hub/question-detail.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def question_edit(request, question_id):
    context = {}
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            data = {
                "question": form.cleaned_data['question'],
                "response_correct": form.cleaned_data['response_correct'],
                "response_incorrect": form.cleaned_data['response_incorrect'],
                "active": form.cleaned_data['active'],
                "question_type": "multiplechoice"
            }
            answers = []
            for i in range(0, 5):
                field = str(i+1)
                if form.cleaned_data["answer_%s_value" % field] != "" \
                        and form.cleaned_data["answer_%s_text" % field] != "":
                    answers.append(
                        {
                            "value": form.cleaned_data["answer_%s_value" % field],  # noqa
                            "text": form.cleaned_data["answer_%s_text" % field],  # noqa
                            "correct": form.cleaned_data["answer_%s_correct" % field]  # noqa
                        }
                    )
            data["answers"] = answers
            if question_id == "new":
                question = clApi.create_question(data)
            else:
                question = clApi.update_question(question_id, data)
            return redirect('question-detail', question_id=question["id"])
    else:
        form = QuestionForm()
        if question_id != "new":
            question = clApi.get_question(question_id)
            form.fields["question"].initial = question["question"]
            form.fields["response_correct"].initial = question["response_correct"]  # noqa
            form.fields["response_incorrect"].initial = \
                question["response_incorrect"]
            form.fields["active"].initial = question["active"]
            if question["answers"] is not None:
                for i in range(0, len(question["answers"])):
                    field = str(i+1)
                    form.fields["answer_%s_value" % field].initial = \
                        question["answers"][i]["value"]
                    form.fields["answer_%s_text" % field].initial = \
                        question["answers"][i]["text"]
                    form.fields["answer_%s_correct" % field].initial = \
                        question["answers"][i]["correct"]

    context.update({
        "form": form
    })
    context.update(csrf(request))
    return render_to_response("hub/question-edit.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def users(request):
    context = {}
    if request.method == "POST":
        form = IdentitiesFilterForm(request.POST)
        if form.is_valid() and form.cleaned_data['code'] is not None:
            identities = idApi.search_identities("details__facility_code",
                                                 form.cleaned_data['code'])
        else:
            identities = idApi.get_identities()
    else:
        form = IdentitiesFilterForm()
        identities = idApi.get_identities()
    context.update({
        "identities": identities,
        "form": form
    })
    context.update(csrf(request))
    return render_to_response("hub/users.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def user_detail(request, user_id):

    context = {}
    identity = idApi.get_identity(user_id)
    context.update({
        "identity": identity
    })
    context.update(csrf(request))
    return render_to_response("hub/user-detail.html",
                              context,
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def facilities(request):
    context = {}
    facilities = FacilityCode.objects.all()
    context.update({
        "facilities": facilities
    })
    context.update(csrf(request))
    return render_to_response("hub/facilities.html",
                              context,
                              context_instance=RequestContext(request))
