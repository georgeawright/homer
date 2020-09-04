from django.http import HttpResponse


def index(request):
    return HttpResponse("This is where you will find information for the saved runs.")
