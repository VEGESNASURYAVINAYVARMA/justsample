from django.urls import path
from .views import CourseListCreateView, CourseDetailView, HelloView

urlpatterns = [
    path("courses/", CourseListCreateView.as_view()),
    path("courses/<int:pk>/", CourseDetailView.as_view()),
    path("hello/", HelloView.as_view()),
]
