from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:run_id>/", views.run_view, name="run"),
    path("<int:run_id>/codelets/", views.codelets_view, name="codelets"),
    path("<int:run_id>/concepts/", views.concepts_view, name="concepts"),
    path("<int:run_id>/codelets/<str:codelet_id>/", views.codelet_view, name="codelet"),
    path(
        "<int:run_id>/concepts/<str:concept_id>/", views.concept_view, name="concept",
    ),
    path(
        "<int:run_id>/perceptlets/<str:perceptlet_id>/",
        views.perceptlet_view,
        name="perceptlet",
    ),
]
