from django.contrib import admin
# <HINT> Import any new Models here
from .models import Course, Enrollment, Lesson, Instructor, Learner, Question, Choice, Submission


# <HINT> Register QuestionInline and ChoiceInline classes here
class ChoiceInLine(admin.StackedInline):
    model = Choice
    # Many-to-many version
    # model = Choice.question.through
    extra = 4


# This class is for explicit aux table LessonQuestion for many-to-many relation
# class LessonQuestionInLine(admin.StackedInline):
#     model = Question.lesson.through

class QuestionInLine(admin.StackedInline):
    model = Question
    # Many-to-many version
    # model = Question.lesson.through
    extra = 3


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


class ChoiceAdmin(admin.ModelAdmin):
    pass


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, QuestionInLine]
    list_display = ('name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']
    # inlines = [LessonQuestionInLine]
    # inlines = [QuestionInLine]


# <HINT> Register Question and Choice models here

# admin.site.register(Choice)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Submission)
admin.site.register(Enrollment)
