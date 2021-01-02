from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView

from . import forms
from . import models

from exam_module import views as main_views

def SignupView(request):
    return render(request, 'registration/signup.html', {})

def SchoolAddView(request):
    if request.method == 'POST':
        add_school_form = forms.SchoolAddForm(request.POST)

        if add_school_form.is_valid():
            add_school = add_school_form.save()

            return redirect(SignupView)

    else:
        add_school_form = forms.SchoolAddForm()

    context_processor = {
                    'add_school_form': add_school_form,
                }

    return render(request, 'registration/school_signup.html', context_processor)


class StudentSignupView(CreateView):
    model = models.User
    form_class = forms.StudentSignupForm
    template_name = 'registration/students_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(main_views.student_view)


class TeacherSignupView(CreateView):
    model = models.User
    form_class = forms.TeacherSignupForm
    template_name = 'registration/teachers_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(main_views.exam_info_view)
