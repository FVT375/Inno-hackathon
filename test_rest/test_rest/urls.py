from django.contrib import admin
from django.urls import path
from . import views
from .utils import Squad, init_models

Squad.init_models()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('squad/', views.ContextQuestionAnswering.as_view()),
    path('correct/', views.AutomaticSpellingCorrection.as_view()),
    path('search/', views.SynonymSearch.as_view())
]