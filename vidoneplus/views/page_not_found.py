from .imports import *


def page_not_found(request, text=None, previous_url=None):
    context = {}
    context['text'] = text
    context['previous_url'] = reverse(f'{previous_url}:{previous_url}s')
    return render(request, '404_page.html', context)
