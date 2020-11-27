from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:run_id>/", views.run_view, name="run"),
    path("<int:run_id>/codelets/", views.codelets_view, name="codelets"),
    path("<int:run_id>/structures/", views.structures_view, name="structures"),
    path(
        "<int:run_id>/coderack_population",
        views.coderack_population_view,
        name="coderack_population",
    ),
    path("<int:run_id>/codelets/<str:codelet_id>/", views.codelet_view, name="codelet"),
    path(
        "<int:run_id>/structures/<str:structure_id>/",
        views.structure_view,
        name="structure",
    ),
]
