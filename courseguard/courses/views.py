from rest_framework import generics, permissions
from rest_framework.throttling import ScopedRateThrottle
from .models import Course
from .serializers import CourseSerializer

from rest_framework.throttling import ScopedRateThrottle

class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer

    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = "course_list"   # 👈 new scope

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Course.objects.all().order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CourseDetailView(generics.RetrieveAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]  # allow GET in Chrome

    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = "course_detail"  # 10/min

    queryset = Course.objects.all()


from rest_framework.views import APIView
from rest_framework.response import Response

class HelloView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"message": "Hello welcome the page"})
