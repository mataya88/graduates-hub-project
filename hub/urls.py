from django.urls import path
from . import views

urlpatterns = [path("allSkills/", views.get_skill_set)]