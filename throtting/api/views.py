from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import Course
from .serializers import CourseSerializer



class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer

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
    permission_classes = [permissions.AllowAny]
    queryset = Course.objects.all()


class HelloView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"message": "Hello welcome the page"})
    
class userView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"message": "Hello welcome the user page"})
    
class profileView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"message": "Hello welcome the user profile page"})
class tempView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"message": "Hello welcome the temp page"})