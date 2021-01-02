from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator

from . import forms
from . import models

from django.contrib.auth.decorators import login_required
from .decorators import teacher_required, student_required

import datetime

# Home Page
def index(request):

    return render(request, 'index.html')


############------------------------ Teacher Views ------------------------############

# Creating the Exam with Exam Name, subject etc...
@login_required
@teacher_required
def exam_info_view(request):

    exam_info_instance = models.Exam_Info.objects.all()

    if request.method == 'POST':
        create_exam_form = forms.Create_Exam_Form(request.POST)

        if create_exam_form.is_valid():
            create_exam = create_exam_form.save()
            exam_name = create_exam_form.cleaned_data['exam_name']

            exam_info = models.Exam_Info.objects.get(exam_name=exam_name)
            exam_info.prepared_by = request.user
            exam_info.save(update_fields=['prepared_by'])

            return redirect(edit_exam_view, exam_id=create_exam.id, exam_name=exam_name)

    else:
        create_exam_form = forms.Create_Exam_Form()

    context_processors = {
                        'create_exam_form': create_exam_form,
                        'exam_info_instance': exam_info_instance,
                    }

    return render(request, 'add_exam.html', context_processors)


# Creating the Exam with Exam Name, subject etc...
@login_required
@teacher_required
def update_exam_info_view(request, exam_id):

    exam_info_instance = models.Exam_Info.objects.get(id=exam_id)

    update_exam_info_form = forms.Create_Exam_Form(request.POST, instance=exam_info_instance)

    if update_exam_info_form.is_valid():
        update_exam_info_form.save()
        return redirect(exam_info_view)

    context_processors={
                    'update_exam_info_form' : update_exam_info_form,
                    'exam_info_instance' : exam_info_instance,
                }

    return render(request, 'update_exam_info.html', context_processors)



# Deleting the Exam itself
@login_required
@teacher_required
def delete_exam_view(request, exam_id, exam_name):

    exam_info_instance = models.Exam_Info.objects.get(id=exam_id)

    exam_info_instance.delete()

    return redirect(exam_info_view)


# To Open Exam Viewing all the questions to edit or delete and saving...
@login_required
@teacher_required
def edit_exam_view(request, exam_id, exam_name):
    if request.method == 'POST':

        create_question_form = forms.Create_Question_Form(request.POST)

        exam_info_instance = models.Exam_Info.objects.get(id=exam_id)
        show_questions_instance = models.Question.objects.filter(exam_info_id=exam_id)

        if create_question_form.is_valid():
            create_question = create_question_form.save()

            question_instance = models.Question.objects.get(pk=create_question.pk)

            #exam_info_id checked from pgadmin table
            question_instance.exam_info = exam_info_instance #exam_id
            question_instance.save(update_fields=['exam_info'])

            return redirect(edit_exam_view, exam_id=exam_id, exam_name=exam_name)

    else:
        create_question_form = forms.Create_Question_Form()
        exam_info_instance = models.Exam_Info.objects.get(exam_name=exam_name)
        show_questions_instance = models.Question.objects.filter(exam_info_id=exam_id)

    context_processors = {
                        'create_question_form' : create_question_form,
                        'show_questions_instance' : show_questions_instance,
                        'exam_id': exam_id,
                    }

    return render(request, 'edit_exam.html', context_processors)


# Updating the Questions in Exam Edit
@login_required
@teacher_required
def update_question_view(request, exam_id, question_id):

    exam_info_instance = models.Exam_Info.objects.get(id=exam_id)
    question_model_instance = models.Question.objects.get(id=question_id)
    create_question_form = forms.Create_Question_Form(request.POST, instance=question_model_instance)

    if create_question_form.is_valid():
        create_question_form.save()
        return redirect(edit_exam_view, exam_id=exam_id, exam_name=exam_info_instance.exam_name)

    context_processors = {
                        'question_model_instance': question_model_instance,
                        'create_question_form': create_question_form,
                    }
    return render(request, 'update_question.html', context_processors)


# Deleting the Questions in Exam Edit
@login_required
@teacher_required
def delete_question_view(request, exam_id, question_id):

    exam_info_instance = models.Exam_Info.objects.get(id=exam_id)
    question_instance = models.Question.objects.get(id=question_id)

    question_instance.delete()

    return redirect(edit_exam_view, exam_id=exam_id, exam_name=exam_info_instance.exam_name)


@login_required
@teacher_required
def show_exam_responses(request):

    exam_info_instance = models.Exam_Info.objects.all()

    context_processors = {
                    'exam_info_instance': exam_info_instance,
                }

    return render(request, 'show_exam_responses.html', context_processors)


@login_required
@teacher_required
def show_students_responses_list(request, exam_id):

    exam_info_instance = models.Exam_Info.objects.get(id=exam_id)
    answers_model_instance = models.Answers.objects.filter(exam_info_id=exam_id)

    context_processors = {
                    'exam_id': exam_id,
                    'answers_model_instance': answers_model_instance,
                }

    return render(request, 'show_students_responses_list.html', context_processors)


@login_required
@teacher_required
def student_wise_responses(request, exam_id, student_id):

    exam_info_instance = models.Exam_Info.objects.get(id=exam_id)
    questions_model_instance = models.Question.objects.filter(exam_info_id=exam_id)
    answers_model_instance = models.Answers.objects.filter(exam_info_id=exam_id, student_name_id=student_id).last()

    # This dictionary passes through the template to display question and answers...
    question_answer_dict = {}

    print(answers_model_instance)

    answer = answers_model_instance.answer_dict

    for question in questions_model_instance:
        try:
            question_answer_dict[question] = answer
        except KeyError:
            question_answer_dict[question] = None

    context_processors = {
                    'exam_id': exam_id,
                    'answers_model_instance': answers_model_instance,
                    'question_answer_dict': question_answer_dict,
                }

    return render(request, 'student_wise_responses.html', context_processors)

# If Teacher delete the response of a student then he is able to give exam again...
@login_required
@teacher_required
def delete_student_response(request, exam_id, student_id):

    answers_model_instance = models.Answers.objects.filter(exam_info_id=exam_id, student_name_id=student_id).last()
    answers_model_instance.delete()

    return redirect(show_students_responses_list, exam_id=exam_id)



############------------------------ Student Views ------------------------############

# Views for Students Only
# Students View
@login_required
@student_required
def student_view(request):

    exam_info_instance = models.Exam_Info.objects.all()

    context_processors={
                    'exam_info_instance': exam_info_instance,
                }

    return render(request, 'students_view.html', context_processors)


# Cheking if the student have taken the exam or not and if activation date is of today...
@login_required
@student_required
def checking_student_response(request, exam_id, student_id):

    check_activation_date = models.Exam_Info.objects.get(id=exam_id)
    user_exam_status = models.Answers.objects.filter(exam_info_id=exam_id)
    user_exam_status_list = []

    for user_exam in user_exam_status:
        user_exam_status_list.append(user_exam.student_name.username)

    if str(request.user) not in user_exam_status_list and check_activation_date.activation_date == datetime.date.today():
        return redirect(answer_the_question_view, exam_id, student_id)
    else:
        return HttpResponse("Your response already submitted. If any problem occur during submitting answers please contact your teacher for help.")

# Answers of the Questions by Students form view
@login_required
@student_required
def answer_the_question_view(request, exam_id, student_id):

    exam_info_instance = models.Exam_Info.objects.get(id=exam_id)
    question_model_instance = models.Question.objects.filter(exam_info_id=exam_id)

    if request.method == 'POST':
        response_data = {}
        answer_the_question_form = forms.Answer_The_Question_Form(question_model_instance, request.POST)
        #answer_the_question_form = forms.Answer_The_Question_Form(len(question_model_instance), request.POST)

        if answer_the_question_form.is_valid():
            answer_form = answer_the_question_form.save()

            answers_model_instance = models.Answers.objects.get(pk=answer_form.pk)

            for question in question_model_instance:
                answer_no = "answer_" + str(question.pk)
                response_data[question.pk] = request.POST.get(answer_no, None)

            try:
                answers_model_instance.student_name = request.user
                answers_model_instance.exam_info = exam_info_instance
                answers_model_instance.answer_dict = response_data
                answers_model_instance.save(update_fields=['exam_info', 'answer_dict', 'student_name'])
            except:
                return HttpResponse("Some Error Occur")

            return redirect(student_view)

    else:
        answer_the_question_form = forms.Answer_The_Question_Form(question_model_instance)
        #answer_the_question_form = forms.Answer_The_Question_Form(len(question_model_instance))

    context_processors={
                'exam_info_instance': exam_info_instance,
                'question_model_instance': question_model_instance,
                'answer_the_question_form': answer_the_question_form,
                'exam_id': exam_id,
            }

    return render(request, 'show_quiz.html', context_processors)
