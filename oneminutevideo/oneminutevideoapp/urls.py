from django.urls import path
from .views import VideoCreateView,AudioGetView

urlpatterns = [
    path('create', VideoCreateView.as_view()),
    path('list', AudioGetView.as_view())
]