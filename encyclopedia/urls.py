from django.urls import path

from . import views


app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("GetRandomEntry", views.getRandomEntry, name="getRandomEntry"),
    path("EditContent/<str:entryTitle>", views.editContent, name="editContent"),
    path("CreateNewEntry", views.createNewEntry, name="createNewEntry"),
    path("ErrorMessage", views.errorMessage, name="errorMessage"),
    path("<str:entryName>", views.viewEntry, name="viewEntry")
]
