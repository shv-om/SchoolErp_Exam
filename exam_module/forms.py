from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from . import models

class Create_Exam_Form(ModelForm):

    class Meta:
        model = models.Exam_Info
        exclude = ['pub_date', 'prepared_by']

        widgets = {
            'exam_name': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_subject': forms.TextInput(attrs={'class': 'form-control'}),
            'prepared_by': forms.TextInput(attrs={'class': 'form-control'}),
            'activation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class Create_Question_Form(ModelForm):

    class Meta:
        model = models.Question
        exclude = ['exam_info']
        #fields = '__all__'

        widgets = {
            'exam_question_types': forms.Select(choices=models.Question.EXAM_QUESTION_TYPES_CHOICES, attrs={'class': 'form-control',}),
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': "6"}),
            'correct_answers': forms.TextInput(attrs={'class': 'form-control'}),
            'wrong_answers': forms.TextInput(attrs={'class': 'form-control'}),
        }

class Answer_The_Question_Form(ModelForm):

    class Meta:
        model = models.Answers
        exclude = ['exam_info', 'student_name', 'answer_dict']

    def __init__(self, question_instance, *args, **kwargs):
        super(Answer_The_Question_Form, self).__init__(*args, **kwargs)

        #for i in range(1, n+1):
            #self.fields["answer_%d" % i] = forms.CharField(required=False, max_length=500)

        for question in question_instance:
            self.fields["answer_%d" % question.id] = forms.CharField(required=False, widget=forms.Textarea(attrs={
                                                                                                            'class': 'form-control',
                                                                                                            'rows': "10",
                                                                                                            'placeholder': "Answer...",
                                                                                                        }))

    def get_answers_fields(self):
        for field_name in self.fields:
            if field_name.startswith('answer_'):
                yield self[field_name]
