import io
import re

from django.db.models import Q
from django.http import HttpResponse
from matplotlib import pyplot
import numpy

from .models import (
    CodeletRecord,
    CoderackRecord,
    ConceptRecord,
    PerceptletRecord,
    PerceptletUpdateRecord,
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
    output += '<p><a href="concepts">Concepts</a></p>'
    output += '<p><a href="perceptlets">Perceptlets</a></p>'
    output += f'<img src="/runs/{run_id}/coderack_population">'
    perceptlet_records = PerceptletRecord.objects.filter(run_id=run_id).all()
    last_column = 0
    last_row = 0
    raw_perceptlets = []
    for record in perceptlet_records:
        if not re.match("^RawPerceptlet", record.perceptlet_id):
            continue
        raw_perceptlets.append(record)
        if record.location[1] > last_row:
            last_row = record.location[1]
        if record.location[2] > last_column:
            last_column = record.location[2]
    raw_perceptlets_matrix = [
        [None for _ in range(last_column + 1)] for _ in range(last_row + 1)
    ]
    for raw_perceptlet in raw_perceptlets:
        row = raw_perceptlet.location[1]
        column = raw_perceptlet.location[2]
        raw_perceptlets_matrix[row][column] = raw_perceptlet
    output += "<h2>Raw Input</h2>"
    output += '<table border="1">'
    for i in range(last_row + 1):
        output += "<tr>"
        for j in range(last_column + 1):
            output += "<td>"
            output += str(raw_perceptlets_matrix[i][j].value)
            output += "</td>"
        output += "</tr>"
    output += "</table>"
    output += "<h2>Labels</h2>"
    output += '<table border="1">'
    for i in range(last_row + 1):
        output += "<tr>"
        for j in range(last_column + 1):
            output += "<td>"
            raw_perceptlet = raw_perceptlets_matrix[i][j]
            output += "".join(
                [
                    f"{connection.value} ({connection.quality[-1]})<br>"
                    for connection in raw_perceptlet.connections.all()
                    if re.match(r"^Label*", connection.perceptlet_id)
                ]
            )
            output += "</td>"
        output += "</tr>"
    output += "</table>"
    groups = [
        perceptlet
        for perceptlet in perceptlet_records
        if re.match("^Group*", perceptlet.perceptlet_id)
    ]
    output += "<h2>Groups</h2>"
    for group in groups:
        output += f"<h3>{group.perceptlet_id}</h3>"
        output += "".join(
            [
                f"{connection.value} ({connection.quality[-1]})<br>"
                for connection in group.connections.all()
                if re.match(r"^Label*", connection.perceptlet_id)
            ]
        )
        output += "".join(
            [
                f"{connection.value} ({connection.quality[-1]})<br>"
                for connection in group.connections.all()
                if re.match(r"^Textlet*", connection.perceptlet_id)
            ]
        )
        output += '<table border="1">'
        for i in range(last_row + 1):
            output += "<tr>"
            for j in range(last_column + 1):
                if group in raw_perceptlets_matrix[i][j].connections.all():
                    output += '<td style="background-color: coral;">'
                else:
                    output += "<td>"
                output += str(raw_perceptlets_matrix[i][j].value)
                output += "</td>"
            output += "</tr>"
        output += "</table>"
    correspondences = [
        perceptlet
        for perceptlet in perceptlet_records
        if re.match(r"^Correspondence*", perceptlet.perceptlet_id)
    ]
    output += "<h2>Correspondences</h2>"
    for correspondence in correspondences:
        output += (
            f"{correspondence.perceptlet_id}: "
            + f"{correspondence.first_argument} "
            + f"--> {correspondence.second_argument} "
        )
        for connection in correspondence.connections.all():
            if re.match(r"^Label*", connection.perceptlet_id):
                output += f"({connection.value})"
        output += "<br>"
    return HttpResponse(output)


def coderack_population_view(request, run_id):
    coderack_record = CoderackRecord.objects.get(run_id=run_id)
    x = coderack_record.codelets_run
    y = coderack_record.population
    pyplot.clf()
    pyplot.title("Coderack Population")
    pyplot.xlabel("Codelets Run")
    pyplot.ylabel("Codelets on Rack")
    pyplot.plot(x, y)
    buf = io.BytesIO()
    pyplot.savefig(buf, format="svg", bbox_inches="tight")
    svg = buf.getvalue()
    buf.close()
    return HttpResponse(svg, content_type="image/svg+xml")


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
    output += "<li>Target Perceptlet: "
    if codelet_record.target_perceptlet is not None:
        output += (
            '<a href="/runs/'
            + str(run_id)
            + "/perceptlets/"
            + codelet_record.target_perceptlet.perceptlet_id
            + '/">'
            + codelet_record.target_perceptlet.perceptlet_id
            + "</a></li>"
        )
    else:
        output += "None</li>"
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


def concepts_view(request, run_id):
    concept_records = ConceptRecord.objects.filter(run_id=run_id).order_by("name")
    output = "<h1>Concepts</h1>"
    output += "<ul>"
    output += "".join(
        [
            '<li><a href="' + concept.concept_id + '">' + concept.name + "</a></li>"
            for concept in concept_records
        ]
    )
    output += "</ul>"
    return HttpResponse(output)


def concept_view(request, run_id, concept_id):
    concept_record = ConceptRecord.objects.get(run_id=run_id, concept_id=concept_id)
    output = "<h1>" + concept_id + "</h1>"
    output += f'<img src="/runs/{run_id}/concepts/{concept_id}/activation">'
    output += "<ul>"
    output += "<li>Activation: " + str(concept_record.activation) + "</li>"
    output += "</ul>"
    return HttpResponse(output)


def concept_activation_view(request, run_id, concept_id):
    concept_record = ConceptRecord.objects.get(run_id=run_id, concept_id=concept_id)
    x = [i for i, j in concept_record.activation]
    y = [numpy.mean(numpy.array(j)) for i, j in concept_record.activation]
    pyplot.clf()
    name = concept_record.name.upper()
    pyplot.title(f"{name} activation")
    pyplot.xlabel("Codelets Run")
    pyplot.ylabel("Concept Activation")
    pyplot.plot(x, y)
    buf = io.BytesIO()
    pyplot.savefig(buf, format="svg", bbox_inches="tight")
    svg = buf.getvalue()
    buf.close()
    return HttpResponse(svg, content_type="image/svg+xml")


def perceptlets_view(request, run_id):
    perceptlet_records = PerceptletRecord.objects.filter(run_id=run_id).order_by(
        "perceptlet_id"
    )
    output = "<h1>Perceptlets</h1>"
    output += "<ul>"
    output += "".join(
        [
            '<li><a href="'
            + perceptlet.perceptlet_id
            + '">'
            + perceptlet.perceptlet_id
            + "</a></li>"
            for perceptlet in perceptlet_records
        ]
    )
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
    if perceptlet_record.parent_codelet is not None:
        output += (
            '<li>Parent Codelet: <a href="/runs/'
            + str(run_id)
            + "/codelets/"
            + perceptlet_record.parent_codelet.codelet_id
            + '">'
            + perceptlet_record.parent_codelet.codelet_id
            + "</a></li>"
        )
    else:
        output += "<li>Parent Codelet: None</li>"
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
                for connection in perceptlet_record.connections.all()
            ]
        )
    output += "<li>Activation: " + str(perceptlet_record.activation) + "</li>"
    output += "<li>Unhappiness : " + str(perceptlet_record.unhappiness) + "</li>"
    output += "<li>Quality: " + str(perceptlet_record.quality) + "</li>"
    output += "</ul>"
    output += "<h2>History</h2>"
    updates = PerceptletUpdateRecord.objects.filter(
        run_id=run_id, perceptlet=perceptlet_record
    ).order_by("time")
    for update in updates:
        output += (
            f"<p>{update.time}: {update.action} by "
            + f'<a href="/runs/{run_id}/codelets/{update.codelet.codelet_id}">'
            + f"{update.codelet.codelet_id}</a>.</p>"
        )
    return HttpResponse(output)
