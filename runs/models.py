from django.db import models

MAX_STRING_LENGTH = 200


class RunRecord(models.Model):
    start_time = models.DateTimeField("Completion Time", auto_now_add=True)


class CodeletRecord(models.Model):
    codelet_id = models.CharField("Codelet ID", max_length=MAX_STRING_LENGTH)
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE)
    codelet_type = models.CharField("Codelet ID", max_length=MAX_STRING_LENGTH)
    birth_time = models.IntegerField("Birth Time")
    time_run = models.IntegerField("Time Run", blank=True, null=True)
    urgency = models.FloatField("Urgency")
    parent = models.ForeignKey(
        "self",
        related_name="+",
        on_delete=models.CASCADE,
        unique=True,
        blank=True,
        null=True,
    )
    perceptlet_types = models.ManyToManyField("ConceptRecord")
    target_perceptlet = models.ForeignKey(
        "PerceptletRecord", on_delete=models.CASCADE, blank=True, null=True
    )
    follow_up = models.ForeignKey(
        "self",
        related_name="Follow Up Codelet+",
        on_delete=models.CASCADE,
        unique=True,
        blank=True,
        null=True,
    )


class CoderackRecord(models.Model):
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE, unique=True)
    codelets_run = models.IntegerField("Codelets Run")
    population = models.IntegerField("Population")


class ConceptRecord(models.Model):
    concept_id = models.CharField("Concept ID", max_length=MAX_STRING_LENGTH)
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=MAX_STRING_LENGTH)
    activation = models.JSONField("Activation")


class PerceptletRecord(models.Model):
    perceptlet_id = models.CharField("Perceptlet ID", max_length=MAX_STRING_LENGTH)
    run_id = models.ForeignKey("RunRecord", on_delete=models.CASCADE)
    time_created = models.IntegerField("Time Created")
    value = models.CharField("Value", max_length=MAX_STRING_LENGTH)
    location = models.JSONField("location", null=True)
    connections = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    activation = models.JSONField("Activation")
    unhappiness = models.JSONField("Unhappiness")
    quality = models.FloatField("quality")
    parent_concept = models.ForeignKey(
        "ConceptRecord", on_delete=models.CASCADE, blank=True, null=True
    )
    parent_codelet = models.ForeignKey(
        "CodeletRecord", on_delete=models.CASCADE, blank=True, null=True
    )
