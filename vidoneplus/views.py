from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import json
from course.models import Course


def IndexPage(request):
    return redirect('/accounts')


@csrf_exempt
def validate_course(request):
    data = {}
    context = {}
    from client.models import Setting as usetting
    from course.models import CourseUser, Course, Lesson, Lesson_file, Teacher, Type_course, Type
    body_unicode = request.body.decode('utf-8')
    if len(body_unicode) != 0:
        body = json.loads(body_unicode)
        data = body['content']
    context['status'] = True
    if len(data) != 0 and usetting.objects.filter(domain=data['domain']).exists():
        user = usetting.objects.get(domain=data['domain']).owner
        list_course = CourseUser.objects.filter(owner=user)
        full_teachers = []
        full_courses = []
        for course in json.loads(data['courses']):
            teacher = course['fields']['teacher']
            if CourseUser.objects.filter(owner=user, course_id=course['pk']).exists():
                courseobj = Course.objects.filter(id=course['pk'], title=course['fields']['title'],
                                                  description=course['fields']['description'],
                                                  subdescription=course['fields']['subdescription'],
                                                  price=course['fields']['price'],
                                                  price_with_discount=course['fields']['price_with_discount'],
                                                  image=course['fields']['image'],
                                                  video=course['fields']['video'],
                                                  extra=course['fields']['extra'],
                                                  free_course=course['fields']['free_course'],
                                                  lesson_count=course['fields']['lesson_count'])
                if courseobj.exists():
                    list_teacher = []
                    for i in courseobj[0].teacher.all():
                        full_teachers.append(i.id)
                        list_teacher.append(i.id)
                    for i in teacher:
                        if i not in list_teacher:
                            context['status'] = False
                    full_courses.append(courseobj[0])
            else:
                context['status'] = False

            if context['status'] == False:
                break
        for teacher in json.loads(data['teachers']):
            if teacher['pk'] not in full_teachers:
                context['status'] = False
            if not Teacher.objects.filter(id=teacher['pk'], name=teacher['fields']['name'],
                                          image=teacher['fields']['image'],
                                          description=teacher['fields']['description']).exists():
                context['status'] = False
            if context['status'] == False:
                break
        for lesson in json.loads(data['lessons']):
            try:
                if Lesson.objects.get(id=lesson['pk']).course not in full_courses:
                    context['status'] = False
                if not Lesson.objects.filter(id=lesson['pk'], course_id=lesson['fields']['course'],
                                             title=lesson['fields']['title'],
                                             order_id=lesson['fields']['order_id']).exists():
                    context['status'] = False
            except:
                context['status'] = False

            if context['status'] == False:
                break
        for lesson_file in json.loads(data['lesson_files']):
            try:
                if Lesson_file.objects.get(id=lesson_file['pk']).lesson.course not in full_courses:
                    context['status'] = False
                if not Lesson_file.objects.filter(id=lesson_file['pk'], lesson_id=lesson_file['fields']['lesson'],
                                                  title=lesson_file['fields']['title'],
                                                  duration=lesson_file['fields']['duration'],
                                                  size=lesson_file['fields']['size'],
                                                  order_id=lesson_file['fields']['order_id'],
                                                  media_type=lesson_file['fields']['media_type'],
                                                  free_lesson=lesson_file['fields']['free_lesson'],
                                                  stream_name=lesson_file['fields']['stream_name'],
                                                  media_file=lesson_file['fields']['media_file']).exists():
                    context['status'] = False
            except:
                context['status'] = False

            if context['status'] == False:
                break
        full_zone = []
        for type_course in json.loads(data['Type_courses']):
            if Type_course.objects.get(id=type_course['pk']).course not in full_courses:
                context['status'] = False
            if not Type_course.objects.filter(id=type_course['pk'], order_id=type_course['fields']['order_id'],
                                              course_id=type_course['fields']['course'],
                                              type_id=type_course['fields']['type']).exists():
                context['status'] = False
            full_zone.append(type_course['fields']['type'])
            if context['status'] == False:
                break
        for zone_list in json.loads(data['zone_lists']):
            if zone_list['pk'] not in full_zone:
                context['status'] = False
            if not Type.objects.filter(id=zone_list['pk'], title=zone_list['fields']['title'],
                                       logo=zone_list['fields']['logo'],
                                       order_id=zone_list['fields']['order_id'],
                                       menu=zone_list['fields']['menu'],
                                       main_type_id=zone_list['fields']['main_type'],
                                       count=zone_list['fields']['count']).exists():
                context['status'] = False
            if context['status'] == False:
                break
    else:
        context['status'] = False
    return JsonResponse(context)
