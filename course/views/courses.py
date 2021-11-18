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
            cu.user = User.objects.get(id=request.user.id)
            cu.status = True
            cu.save()
    courses = CourseUser.objects.values_list('course', flat=True).filter(owner=request.user)
    courses = Course.objects.filter(id__in=courses)
    lessons = Lesson.objects.filter(course__in=courses)
    lesson_files = Lesson_file.objects.filter(lesson__in=lessons)
    # print(courses, lessons, lessons_file)
    domain = Setting.objects.get(owner=request.user).domain
    print(domain)
    contextupload = {}
    contextupload['courses'] = serializers.serialize("json", courses)
    contextupload['lessons'] = serializers.serialize("json", lessons)
    contextupload['lesson_files'] = serializers.serialize("json", lesson_files)
    response = requests.post('https://%s/update_course/'%(domain), data=json.dumps(contextupload))
    return render(request, "client/course.html", context)
