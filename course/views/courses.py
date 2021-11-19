import json

from client.views.imports import *
from client.models import *
from course.models import *
from django.core import serializers
import requests


@login_required
def courses(request):
    context = {}
    context['courses'] = Course.objects.all()
    if request.method == 'POST':
        context['user'] = request.user
        countcheck = request.POST.getlist('course_records')
        for item in countcheck:
            cu = CourseUser()
            cu.course = Course.objects.get(id=item)
            cu.owner = User.objects.get(id=request.user.id)
            cu.status = True
            cu.save()
        # domain = Setting.objects.get(owner=request.user).domain
        courses = CourseUser.objects.values_list('course', flat=True).filter(owner=request.user)
        courses = Course.objects.filter(id__in=courses)
        teachers = []
        for course in courses:
            for tchr in course.teacher.all():
                teachers.append(tchr.id)
        teachers = Teacher.objects.filter(id__in=teachers)
        lessons = Lesson.objects.filter(course__in=courses)
        lesson_files = Lesson_file.objects.filter(lesson__in=lessons)
        type_courses = Type_course.objects.filter(course__in=courses)
        zone_lists = []
        for i in type_courses:
            zone_lists.append(i.type.id)
        zone_lists = Type.objects.filter(id__in=zone_lists)
        contextupload = {}
        contextupload['courses'] = serializers.serialize("json", courses)
        contextupload['lessons'] = serializers.serialize("json", lessons)
        contextupload['lesson_files'] = serializers.serialize("json", lesson_files)
        contextupload['teachers'] = serializers.serialize("json", teachers)
        contextupload['Type_courses'] = serializers.serialize("json", type_courses)
        contextupload['zone_lists'] = serializers.serialize("json", zone_lists)
        response = requests.post('https://%s/update_course/'%(domain), data=json.dumps(contextupload))
        # response = requests.post('http://127.0.0.1:8000/update_course/', data=json.dumps(contextupload))
    return render(request, "client/course.html", context)
