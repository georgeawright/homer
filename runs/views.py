from django.db.models import Q
from django.http import HttpResponse

from .models import (
    CodeletRecord,
    CoderackRecord,
    ConceptRecord,
    PerceptletRecord,
    RunRecord,
)


def index(request):
    runs = RunRecord.objects.order_by("-start_time")
    list_of_runs = "".join(
        [
            '<a href="' + str(run.id) + '"><li>' + str(run.start_time) + "</li></a>"
            for run in runs
        ]
    )
    output = "<ul>" + list_of_runs + "</ul>"
    return HttpResponse(output)


def run_view(request, run_id):
    coderack_record = CoderackRecord.objects.get(run_id=run_id)
    output = "<h1>Basic Run information:</h1>"
    output += "<ul>"
    output += "<li>Codelets Run: " + str(coderack_record.codelets_run[-1])
    output += "</ul>"
    output += '<p><a href="codelets">Codelets</a></p>'
    return HttpResponse(output)


def codelets_view(request, run_id):
    codelet_records = (
        CodeletRecord.objects.filter(run_id=run_id)
        .filter(~Q(time_run=None))
        .order_by("time_run")
    )
    output = "<h1>Codelets in order run</h1>"
    output += "<ul>"
    output += "".join(
        [
            '<li><a href="'
            + codelet.codelet_id
            + '">'
            + codelet.codelet_id
            + "</a></li>"
            for codelet in codelet_records
        ]
    )
    output += "</ul>"
    return HttpResponse(output)


def codelet_view(request, run_id, codelet_id):
    codelet_record = CodeletRecord.objects.get(run_id=run_id, codelet_id=codelet_id)
    output = "<h1>" + codelet_id + "</h1>"
    output += "<ul>"
    output += "<li>Birth Time: " + str(codelet_record.birth_time) + "</li>"
    output += "<li>Time Run: " + str(codelet_record.time_run) + "</li>"
    output += "<li>Urgency: " + str(codelet_record.urgency) + "</li>"
    output += "<li>Parent Codelet: "
    if codelet_record.parent is not None:
        output += (
            '<a href="/runs/'
            + str(run_id)
            + "/codelets/"
            + codelet_record.parent.codelet_id
            + '/">'
            + codelet_record.parent.codelet_id
            + "</a></li>"
        )
    else:
        output += "None</li>"
    output += "<li>Follow up: "
    try:
        follow_up = CodeletRecord.objects.get(run_id=run_id, parent=codelet_record)
        output += (
            '<a href="/runs/'
            + str(run_id)
            + "/codelets/"
            + follow_up.codelet_id
            + '/">'
            + follow_up.codelet_id
            + "</a></li>"
        )
    except CodeletRecord.DoesNotExist:
        output += "None</li>"
    output += "<li>Child Perceptlet: "
    try:
        child_perceptlet = PerceptletRecord.objects.get(
            run_id=run_id, parent_codelet=codelet_record.id
        )
        output += (
            '<a href="/runs/'
            + str(run_id)
            + "/perceptlets/"
            + child_perceptlet.perceptlet_id
            + '/">'
            + child_perceptlet.perceptlet_id
            + "</a></li>"
        )
    except PerceptletRecord.DoesNotExist:
        output += "None</li>"
    output += "</ul>"
    return HttpResponse(output)


def perceptlet_view(request, run_id, perceptlet_id):
    perceptlet_record = PerceptletRecord.objects.get(
        run_id=run_id, perceptlet_id=perceptlet_id
    )
    output = "<h1>" + perceptlet_id + "</h1>"
    output += "<ul>"
    output += "<li>Birth Time: " + str(perceptlet_record.time_created) + "</li>"
    output += "<li>Value: " + perceptlet_record.value + "</li>"
    output += "<li>Location: " + str(perceptlet_record.location) + "</li>"
    output += (
        '<li>Parent Codelet: <a href="/runs/'
        + str(run_id)
        + "/codelets/"
        + perceptlet_record.parent_codelet.codelet_id
        + '">'
        + perceptlet_record.parent_codelet.codelet_id
        + "</a></li>"
    )
    if perceptlet_record.parent_concept is not None:
        output += (
            '<li>Parent Concept: <a href="/runs/'
            + str(run_id)
            + "/concepts/"
            + perceptlet_record.parent_concept.concept_id
            + '">'
            + perceptlet_record.parent_concept.concept_id
            + "</a></li>"
        )
    else:
        output += "<li>Parent Concept: None</li>"
    if perceptlet_record.connections is None:
        output += "<li>Connections: None</li>"
    else:
        output += "<li>Connections: " + ", ".join(
            [
                '<a href="/runs/'
                + str(run_id)
                + "/perceptlets/"
                + connection.perceptlet_id
                + '">'
                + connection.perceptlet_id
                + "</a></li>"
                for connection in perceptlet_record.connections
            ]
        )
    output += "<li>Activation: " + str(perceptlet_record.activation) + "</li>"
    output += "<li>Unhappiness : " + str(perceptlet_record.unhappiness) + "</li>"
    output += "<li>Quality: " + str(perceptlet_record.quality) + "</li>"
    output += "</ul>"
    return HttpResponse(output)


def concept_view(request, run_id, concept_id):
    concept_record = ConceptRecord.objects.get(run_id=run_id, concept_id=concept_id)
    output = "<h1>" + concept_id + "</h1>"
    output += "<ul>"
    output += "<li>Activation: " + str(concept_record.activation) + "</li>"
    output += "</ul>"
    return HttpResponse(output)
