from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator

from . import forms
from . import models

# Creating the Exam with Exam Name, subject etc...
# Rename to Teachers View later
def exam_info_view(request):
    if request.method == 'POST':
        create_exam_form = forms.Create_Exam_Form(request.POST)
        exam_info_instance = models.Exam_Info.objects.all()

        if create_exam_form.is_valid():
            create_exam = create_exam_form.save()
            exam_name = create_exam_form.cleaned_data['exam_name']
            return redirect(edit_exam_view, exam_id=create_exam.id, exam_name=exam_name)

    else:
        create_exam_form = forms.Create_Exam_Form()
        exam_info_instance = models.Exam_Info.objects.all()

    context_processors = {
                        'create_exam_form': create_exam_form,
                        'exam_info_instance': exam_info_instance,
                    }

    return render(request, 'add_exam.html', context_processors)

# Deleting the Exam itself
def delete_exam_view(request, exam_id, exam_name):

    exam_info_instance = models.Exam_Info.objects.get(id=exam_id)

    exam_info_instance.delete()

    return redirect(exam_info_view)

# To Open Exam Viewing all teh questions to edit or delete and saving...
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
def delete_question_view(request, exam_id, question_id):

    exam_info_instance = models.Exam_Info.objects.get(id=exam_id)
    question_instance = models.Question.objects.get(id=question_id)

    question_instance.delete()

    return redirect(edit_exam_view, exam_id=exam_id, exam_name=exam_info_instance.exam_name)

# Students View
def student_view(request):

    exam_info_instance = models.Exam_Info.objects.all()

    context_processors={
                    'exam_info_instance': exam_info_instance,
                }

    return render(request, 'students_view.html', context_processors)


# Answers of the Questions by Students form view
def answer_the_question_view(request, exam_id):

    exam_info_instance = models.Exam_Info.objects.get(id=exam_id)
    question_model_instance = models.Question.objects.filter(exam_info_id=exam_id)
    paginator_questions = Paginator(question_model_instance, 1)

    question_page_no = request.GET.get('question_no')

    try:
        question_page_object = paginator_questions.get_page(question_page_no)
    except PageNotAnInteger:
        question_page_object = paginator_questions.get_page(1)
    except EmptyPage:
        question_page_object = paginator_questions.get_page(paginator.num_pages)

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
                answers_model_instance.exam_info = exam_info_instance
                answers_model_instance.answer_dict = response_data
                answers_model_instance.save(update_fields=['exam_info', 'answer_dict'])
            except:
                print("Some Error Occur")

            return JsonResponse(response_data)

        else:
            response_data['error'] = True
            response_data['message'] = "Some Error Occur"
            return JsonResponse(response_data)

    else:
        answer_the_question_form = forms.Answer_The_Question_Form(question_model_instance)
        #answer_the_question_form = forms.Answer_The_Question_Form(len(question_model_instance))

    context_processors={
                'question_model_instance': question_model_instance,
                'answer_the_question_form': answer_the_question_form,
                'exam_id': exam_id,
                'question_page_object': question_page_object,
            }

    return render(request, 'show_quiz.html', context_processors)
