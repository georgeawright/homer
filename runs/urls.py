from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:run_id>/", views.run_view, name="run"),
    path(
        "<int:run_id>/activity-and-structure-concepts/",
        views.activity_and_structure_concepts_view,
        name="codelets",
    ),
    path("<int:run_id>/codelets/", views.codelets_view, name="codelets"),
    path("<int:run_id>/structures/", views.structures_view, name="structures"),
    path(
        "<int:run_id>/run-summary-graphs",
        views.run_summary_graphs_view,
        name="run-summary-graphs",
    ),
    path("<int:run_id>/codelets/<str:codelet_id>/", views.codelet_view, name="codelet"),
    path(
        "<int:run_id>/structures/<str:structure_id>/",
        views.structure_view,
        name="structure",
    ),
    path(
        "<int:run_id>/structures-series/<str:structure_id>/",
        views.structure_graphs_view,
        name="structure-graphs",
    ),
]
