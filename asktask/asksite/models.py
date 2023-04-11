from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Q


class QuestionManager(models.Manager):
    def get_hot(self):
        objs = super().all()
        objs = objs.annotate(rating=Count("questionlike"))
        
        return objs.order_by("-rating")

    def get_new(self):
        return super().all().order_by("-date")

class TagManager(models.Manager):
    def get_all_questions(self, tag_name):
        objs = super().all()
        return objs.get(name=tag_name).question_set.all()
    
    def get_top(self):
        objs = super().all()
        objs = objs.annotate(counter=Count("question"))

        return objs.order_by("-counter")

class ProfileManager(models.Manager):
    def get_top(self):
        objs = super().all()
        objs = objs.annotate(user_rating=Count("question"))
        
        return objs.order_by("-user_rating")


class Profile(models.Model):
    name = models.CharField(max_length=30)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
    signup_date = models.DateTimeField(auto_now_add=True)
    objects = ProfileManager()


    def __str__(self):
        return self.name


    def questions(self):
        return self.question_set


class Tag(models.Model):
    name = models.CharField(max_length=30)
    objects = TagManager()

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    author = models.ForeignKey("Profile", on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag")
    date = models.DateTimeField(auto_now_add=True)
    objects = QuestionManager()


    def __str__(self):
        return self.title


    def rating(self):
        return self.questionlike_set.count()
    

    def answers_count(self):
        return self.answer_set.count()


    def all_answers(self):
        return self.answer_set.all()


class Answer(models.Model):
    title = models.CharField(max_length=30)
    text = models.TextField()
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    author = models.ForeignKey("Profile", on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class QuestionLike(models.Model):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    liker = models.ForeignKey("Profile", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
