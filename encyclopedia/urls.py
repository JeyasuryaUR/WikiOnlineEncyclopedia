from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/createnew", views.create_page, name="create_page"),
    path("wiki/random", views.random_page, name="random_page"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit"),
    path("wiki/<str:title>", views.visit_page, name="visit_page")
]
