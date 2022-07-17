from django.shortcuts import render
from django.http import HttpResponseRedirect
# <HINT> Import any new Models here
from .models import Course, Enrollment, Lesson, Question, Choice, Submission
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


# CourseListView
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        # for course in courses:
        #     if users.is_authenticated:
        #         course.is_enrolled = check_if_enrolled(users, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()

    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))


def submit(request, course_id):
    if request.method == "POST":
        user = request.user
        course = get_object_or_404(Course, pk=course_id)
        enrollment = Enrollment.objects.get(user=user, course=course)
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in extract_answers(request):
            choice = Choice.objects.get(pk=choice_id)
            submission.choices.add(choice)
            submission.save()
        return HttpResponseRedirect(reverse(viewname='onlinecourse:show_exam_result', args=(course.id, submission.id)))


# This function for selected answers
def extract_answers(request):
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_answers.append(choice_id)
    return submitted_answers


def show_exam_result(request, course_id, submission_id):
    context = {}
    course = Course.objects.get(pk=course_id)
    submission = Submission.objects.get(pk=submission_id)
    choices = submission.choices.all()

    # Get selected choice ids
    #
    selected_ids = []
    for choice in choices:
        selected_ids.append(choice.id)

    # For each question, check if choices were correct
    correct_questions = []
    max_grade = 0
    for question in course.question_set.all():
        question_is_correct = True
        max_grade += question.grade
        for choice in question.choice_set.all():
            if (not choice.is_correct and choice.id in selected_ids) or (
                    choice.is_correct and choice.id not in selected_ids):
                question_is_correct = False
                break
        if question_is_correct:
            correct_questions.append(question)

    # Calculate grade
    # it would append the results to the total score
    total_score = 0
    for question in correct_questions:
        total_score += question.grade
    print(max_grade)
    print(total_score)
    grade = total_score * 100 / max_grade

    # would select and add the following
    # Add the course, selected_ids, and grade to context for rendering HTML page
    context["course"] = course
    context["selected_ids"] = selected_ids
    context["grade"] = grade
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)


def clean(request):
    Course.objects.all().delete()
    Lesson.objects.all().delete()
    Question.objects.all().delete()
    Choice.objects.all().delete()
    Enrollment.objects.all().delete()
    return HttpResponseRedirect(reverse(viewname="onlinecourse:index"))
