from django.http import HttpResponse

from .models import RunRecord


def index(request):
    runs = RunRecord.objects.order_by("-completion_time")
    list_of_runs = "<li>".join([run.completion_time + "</li>" for run in runs])
    output = "<ul>" + list_of_runs + "</ul>"
    return HttpResponse(output)
