from django.shortcuts import render,get_object_or_404
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .permissions import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token



def index(request):
    return render(request, 'index.html')

class AllStudents(APIView):

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "student": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, uuid=None):
        if uuid:
            student = Student.objects.get(uuid=uuid)
            serializer = StudentSerializer(student)
            return Response({"status": "success", "student": serializer.data}, status=status.HTTP_200_OK)

        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response({"status": "success", "students": serializer.data}, status=status.HTTP_200_OK)   

    def put(self, request, uuid=None):
        student = Student.objects.get(uuid=uuid)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "student": serializer.data})
        else:
            return Response({"status": "error", "student": serializer.errors})


    def delete(self, request, uuid=None):
        student = get_object_or_404(Student, uuid=uuid)
        student.delete()
        return Response({"status": "success", "success": "student Deleted"})
    

class MyUsers(APIView):
    
    def get(self, request, pk=None):
        if pk:
            user = SystemUser.objects.get(id=pk)
            serializer = UserSerializer(user)
            return Response({"status": "success", "user": serializer.data}, status=status.HTTP_200_OK)

        user = SystemUser.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response({"status": "success", "users": serializer.data}, status=status.HTTP_200_OK) 
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "user": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request, pk=None):
        user = SystemUser.objects.get(id=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "user": serializer.data})
        else:
            return Response({"status": "error", "error": serializer.errors})
        
    def delete(self, request, uuid=None):
        user = get_object_or_404(SystemUser, uuid=uuid)
        user.delete()
        return Response({"status": "success", "success": "user Deleted"})
        
        
class ClassroomData(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ClassroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "classroom": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, pk=None):
        if pk:
            classroom = Classroom.objects.get(id=pk)
            serializer = ClassroomSerializer(classroom)
            return Response({"status": "success", "classroom": serializer.data}, status=status.HTTP_200_OK)

        classrooms = Classroom.objects.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response({"status": "success", "classrooms": serializer.data}, status=status.HTTP_200_OK)   

    def put(self, request, pk=None):
        classroom = Classroom.objects.get(id=pk)
        serializer = ClassroomSerializer(classroom, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "classroom": serializer.data})
        else:
            return Response({"status": "error", "error": serializer.errors})


    def delete(self, request, uuid=None):
        classroom = get_object_or_404(Classroom, id=id)
        classroom.delete()
        return Response({"status": "success", "success": "classroom Deleted"})       
        
        
class AuthUsers(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.SystemUser.username),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)       
        
             
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': SystemUser.username,
            'first_name': SystemUser.first_name,
            'last_name': SystemUser.last_name,
            'user_id': SystemUser.pk,
            'email': SystemUser.email
        })     
        
        
        
        
        
        
        
        
        
        