from django.shortcuts import render

from . import models

def index(request):
    questions = models.Question.objects.get_new()
    tags = models.Tag.objects.get_top()
    members = models.Profile.objects.get_top()
    context = {"questions": questions, "tags" : tags, "members" : members}

    return render(request, "index.html", context=context)


def ask(request):
    tags = models.Tag.objects.get_top()
    members = models.Profile.objects.get_top()
    context = { "members": members, "tags" : tags }

    return render(request, "ask.html", context=context)


def login(request):
    tags = models.Tag.objects.get_top()
    members = models.Profile.objects.get_top()
    context = { "members": members, "tags" : tags }

    return render(request, "login.html", context=context)


def question(request, question_id):
    # if (question_id > models.Question.objects.count() or question_id == 0):
    #     return render(request, "404.html")
    
    try :
        tags = models.Tag.objects.get_top()
        members = models.Profile.objects.get_top()
        question = models.Question.objects.get(id=question_id)
        context = { "question": question, "members": members, "tags" : tags }
    except:
        return render(request, "404.html")

    return render(request, "question.html", context=context)


def settings(request):
    tags = models.Tag.objects.get_top()
    members = models.Profile.objects.get_top()
    context = { "members" : members, "tags" : tags }

    return render(request, "settings.html", context=context)


def signup(request):
    tags = models.Tag.objects.get_top()
    members = models.Profile.objects.get_top()
    context = { "members" : members, "tags" : tags }

    return render(request, "signup.html", context=context)


def tags(request, tag_name):
    try:
        tags = models.Tag.objects.get_top()
        members = models.Profile.objects.get_top()
        questions = models.Tag.objects.get_all_questions(tag_name)
        context = { "tag_name": tag_name, "questions" : questions, "members" : members, "tags" : tags }
    except Exception:
        return render(request, "404.html")
    
    return render(request, "tags.html", context=context)


def hot(request):
    tags = models.Tag.objects.get_top()
    members = models.Profile.objects.get_top()
    questions = models.Question.objects.get_hot()
    context = { "questions": questions, "members" : members, "tags" : tags }

    return render(request, "hot.html", context=context)

# Create your views here.
