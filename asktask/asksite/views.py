from django.shortcuts import render

from . import models

def index(request):
    context = {"questions": models.QUESTIONS}
    return render(request, "index.html", context=context)


def ask(request):
    return render(request, "ask.html")


def login(request):
    return render(request, "login.html")


def question(request, question_id):
    if (question_id >= len(models.QUESTIONS)):
        return render(request, "404.html")
    
    context = { "question": models.QUESTIONS[question_id], "answers" : models.ANSWERS }
    return render(request, "question.html", context=context)


def settings(request):
    return render(request, "settings.html")


def signup(request):
    return render(request, "signup.html")


def tags(request, tag_name):
    context = { "tag_name": tag_name, "questions" : models.QUESTIONS }
    return render(request, "tags.html", context=context)


def hot(request):
    context = {"questions": models.QUESTIONS}
    return render(request, "hot.html", context=context)

# Create your views here.
