from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

from registration import models as user_model

class Exam_Info(models.Model):
    exam_name = models.CharField(max_length=25, unique=True)
    exam_subject = models.CharField(max_length=25)
    pub_date = models.DateField(auto_now_add=True)
    activation_date = models.DateField()
    prepared_by = models.ForeignKey(user_model.User, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.exam_name

class Question(models.Model):
    OB = 'Objective'
    SB = 'Subjective'

    EXAM_QUESTION_TYPES_CHOICES = [
        ('SB', 'Subjective'),
        ('OB', 'Objective'),
    ]

    exam_info = models.ForeignKey(Exam_Info, on_delete=models.CASCADE, default=None, null=True)
    exam_question_types = models.CharField(max_length=5, choices=EXAM_QUESTION_TYPES_CHOICES, default=SB,)
    question = models.TextField()
    # Answer fields
    correct_answers = ArrayField(models.CharField(max_length=200), size=8, null=True, blank=True)
    wrong_answers = ArrayField(models.CharField(max_length=200), size=8, null=True, blank=True)

    def __str__(self):
        return self.question

class Answers(models.Model):
    exam_info = models.ForeignKey(Exam_Info, on_delete=models.CASCADE, default=None, null=True)
    student_name = models.ForeignKey(user_model.User, on_delete=models.CASCADE, default=None, null=True)
    answer_dict = JSONField(default=None, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student_name)
