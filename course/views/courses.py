import json

from client.views.imports import *
from client.models import *
from course.models import *
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import requests

NUM_OF_COURSES_PER_PAGE = 15

@login_required
def courses(request):
    context = {}
    page_courses = Course.objects.filter(extra__status=True)
    p = Paginator(page_courses, NUM_OF_COURSES_PER_PAGE)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context['courses'] = {'page_obj': page_obj}
    if request.method == 'POST':
        context['user'] = request.user
        countcheck = request.POST.getlist('course_records')
        for item in countcheck:
            cu = CourseUser()
            cu.course = Course.objects.get(id=item)
            cu.owner = User.objects.get(id=request.user.id)
            cu.status = True
            cu.save()
        domain = Setting.objects.get(owner=request.user).domain
        courses = CourseUser.objects.values_list('course', flat=True).filter(owner=request.user)
        courses = Course.objects.filter(id__in=courses)
        teachers = []
        for course in courses:
            for tchr in course.teacher.all():
                teachers.append(tchr.id)
        teachers = Teacher.objects.filter(id__in=teachers)
        type_courses = Type_course.objects.filter(course__in=courses)
        zone_lists = []
        for i in type_courses:
            zone_lists.append(i.type.id)
        zone_lists = Type.objects.filter(id__in=zone_lists)
        contextupload = {}
        fields = {'courses', 'lessons', 'lesson_files', 'teachers', 'Type_courses', 'zone_lists'}
        for value in fields:
            contextupload[value] = serializers.serialize("json", value)
        response = requests.post('https://%s/update_course/'%(domain), data=json.dumps(contextupload))
    return render(request, "client/course.html", context)
