from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    the_date = models.DateTimeField('the date')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)