from django.db import models

MAX_STRING_LENGTH = 200


class Run(models.Model):
    completion_time = models.DateTimeField("Completion Time")


class Codelet(models.Model):
    codelet_id = models.CharField(
        "Codelet ID", max_length=MAX_STRING_LENGTH, primary_key=True
    )
    run_id = models.ForeignKey("Run", on_delete=models.CASCADE, unique=True)
    codelet_type = models.CharField("Codelet ID", max_length=MAX_STRING_LENGTH)
    time_run = models.IntegerField("Time Run")
    urgency = models.FloatField("Urgency")
    parent = models.ForeignKey(
        "self", related_name="+", on_delete=models.CASCADE, unique=True
    )
    perceptlet_types = models.ManyToManyField("Concept")
    target_perceptlet = models.ForeignKey("Perceptlet", on_delete=models.CASCADE)
    follow_up = models.ForeignKey(
        "self", related_name="Follow Up Codelet+", on_delete=models.CASCADE, unique=True
    )


class Concept(models.Model):
    concept_id = models.CharField(
        "Concept ID", max_length=MAX_STRING_LENGTH, primary_key=True
    )
    run_id = models.ForeignKey("Run", on_delete=models.CASCADE, unique=True)
    name = models.CharField("Name", max_length=MAX_STRING_LENGTH)
    activation = models.ForeignKey("ActivationPattern", on_delete=models.CASCADE)


class Perceptlet(models.Model):
    perceptlet_id = models.CharField(
        "Perceptlet ID", max_length=MAX_STRING_LENGTH, primary_key=True
    )
    run_id = models.ForeignKey("Run", on_delete=models.CASCADE, unique=True)
    time_created = models.IntegerField("Time Created")
    value = models.CharField("Value", max_length=MAX_STRING_LENGTH)
    connections = models.ForeignKey("self", on_delete=models.CASCADE)
    activation = models.ForeignKey("ActivationPattern", on_delete=models.CASCADE)
    unhappiness = models.ForeignKey(
        "ActivationPattern", related_name="+", on_delete=models.CASCADE
    )
    quality = models.JSONField("quality")
    parent_concept = models.ForeignKey("Concept", on_delete=models.CASCADE)
    parent_codelet = models.ForeignKey("Codelet", on_delete=models.CASCADE)


class ActivationPattern(models.Model):
    run_id = models.ForeignKey("Run", on_delete=models.CASCADE, unique=True)
    series = models.JSONField("Series")
