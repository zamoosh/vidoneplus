from .imports import *
from ..models import *


@login_required
def courses(request):
    context = {}
    context['courses'] = CourseVitrin.objects.all()
    if request.method == 'POST':
        context['user'] = request.user
        countcheck = request.POST.getlist('course_records')
        for item in countcheck:
            cu = CourseUser()
            cu.course = CourseVitrin.objects.get(id=item)
            cu.user = User.objects.get(id=request.user.id)
            cu.status = True
            cu.save()
    # context['all_cu'] = CourseUser.objects.filter(user=request.user)
    return render(request, "client/course.html", context)
