from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('squad/', views.ContextQuestionAnswering.as_view()),
    path('correct/', views.AutomaticSpellingCorrection.as_view())
]