from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)    


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class UserProfile(models.Model): 
    user = models.ForeignKey(User,unique=True)
    name = models.CharField(max_length=30)
    occupation = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    province = models.CharField(max_length=50)
    sex = models.CharField(max_length=1)

    def __str__(self):
        return self.name

