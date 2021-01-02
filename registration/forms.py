from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from . import models

class SchoolAddForm(forms.ModelForm):

    class Meta:
        model = models.School_Info
        fields = '__all__'

        widgets = {
            'school_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'school_address': forms.Textarea(attrs={'class': 'form-control'}),
        }


class StudentSignupForm(UserCreationForm):

    grade = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    school_info = forms.ModelChoiceField(queryset=models.School_Info.objects.all(), empty_label=" - - - Choose School Name - - - ")

    class Meta(UserCreationForm.Meta):
        model = models.User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.school_info = self.cleaned_data.get('school_info')
        user.save()

        student = models.Student.objects.create(user=user)
        student.grade = self.cleaned_data.get('grade')
        student.save(update_fields=['grade'])

        return user


class TeacherSignupForm(UserCreationForm):

    subject = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    school_info = forms.ModelChoiceField(queryset=models.School_Info.objects.all(), empty_label=" - - - Choose School Name - - - ")

    class Meta(UserCreationForm.Meta):
        model = models.User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.school_info = self.cleaned_data.get('school_info')
        user.save()

        teacher = models.Teacher.objects.create(user=user)
        teacher.subject = self.cleaned_data.get('subject')
        teacher.save(update_fields=['subject'])

        return user
