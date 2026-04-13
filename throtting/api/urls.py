from django.urls import path
from .views import CourseListCreateView, CourseDetailView, HelloView, userView,profileView,tempView, userlevelView
from .views import userleveloneView
urlpatterns = [
    path("hello/", HelloView.as_view()),
    path("user/", userView.as_view()),
    path("profile/",profileView.as_view()),
    path("userlevel/", userlevelView.as_view()),
    path("temp/", tempView.as_view()),
    path("userlevelone/", userleveloneView.as_view()),


   

    path("courses/", CourseListCreateView.as_view()),
    path("courses/<int:pk>/", CourseDetailView.as_view()),
]
