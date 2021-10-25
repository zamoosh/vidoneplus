from django.shortcuts import redirect


def IndexPage(request):
    return redirect('/accounts')
