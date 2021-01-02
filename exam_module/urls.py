from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('exam_info_view', views.exam_info_view, name='exam_info_view'),
    path('<int:exam_id>/update_exam_info/', views.update_exam_info_view, name='update_exam_info_view'),
    path('<int:exam_id>/<exam_name>/delete_exam', views.delete_exam_view, name='delete_exam_view'),
    path('<int:exam_id>/<exam_name>/edit_exam', views.edit_exam_view, name='edit_exam_view'),
    path('<int:exam_id>/update/<int:question_id>', views.update_question_view, name='update_question_view'),
    path('<int:exam_id>/delete/<int:question_id>', views.delete_question_view, name='delete_question_view'),
    path('show_exam_responses', views.show_exam_responses, name='show_exam_responses'),
    path('<int:exam_id>/show_students_responses_list', views.show_students_responses_list, name='show_students_responses'),
    path('<int:exam_id>/student_wise_responses/<int:student_id>', views.student_wise_responses, name='student_wise_responses'),
    path('<int:exam_id>/delete_response/<int:student_id>', views.delete_student_response, name='delete_student_response'),

    path('student_view', views.student_view, name='student_view'),
    path('<int:exam_id>/quiz/<int:student_id>', views.answer_the_question_view, name='answer_the_question_view'),
    path('<int:exam_id>/checking_student_response/<int:student_id>', views.checking_student_response, name='checking_student_response'),
]
