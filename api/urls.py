from django.urls import path

from . import views


urlpatterns = [
path("recipes/",views.GetRecipes.as_view(),name = "recipes-list"),
path("recipes/<int:id>/",views.GetRecipes.as_view(),name = "recipes-list"),
path("recipes/scrape/",views.RecipeScrapeView.as_view(),name = "scrape-recipe"),
path("notes/",views.NoteListCreate.as_view(),name = "note-list"),
path("notes/delete/<int:pk>",views.NoteDelete.as_view(),name = "delte-note"),
]
