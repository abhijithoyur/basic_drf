from .models import *
from .serializer import PersonSerializers, RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination


# class based function for get, post methods.
class ClassPerson(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        obj = Person.objects.all()
        serializer = PersonSerializers(obj,many = True) #many = True is used when serializer expects a queryset or a list of instance (Which means query set expects multiple instance, if many = False then serializer expects a single instance)
        response_data = {
            'message': "Fetched successfully",
            'status' : 'success',
            'data' : serializer.data
            }
        return Response(response_data,status=status.HTTP_200_OK)
    def post(self, request):
        return Response("This is a post method from APIView")
    
#Register Method
class Register(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        serializer.save()
        return Response({'message':'User Created'}, status=status.HTTP_201_CREATED)
    
#Login Method 
class Login(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response({'message':serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        print(serializer.data)
        user = authenticate(username= serializer.data['username'], password=serializer.data['password'])
        print(user)
        if not user:
            return Response({'message': "Invalid"}, status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        return Response({'message': 'Login successfull', 'token': str(token)}, status=status.HTTP_200_OK)

#Pagination
class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page' #This is what we passes in url of the browser after the path with questionmark(?page=5), we can use any variable instead of 'page'.


@api_view(['GET','POST'])
def index(request):
    if request.method == 'POST':
        data = {
            "name": "John Doe",
            "age": 30,
            "is_employee": True,
            "email": "johndoe@example.com",
            "address": {
                "street": "123 Main St",
                "city": "Springfield",
                "state": "IL",
                "zip": "62704"
            },
            "phone_numbers": [
                "555-1234",
                "555-5678"
            ],
            "projects": [
                {
                    "name": "Project Alpha",
                    "start_date": "2023-01-15",
                    "end_date": "2023-06-30",
                    "budget": 50000
                },
                {
                    "name": "Project Beta",
                    "start_date": "2023-07-01",
                    "end_date": "2024-01-15",
                    "budget": 75000
                }
            ],
            "skills": [
                "Python",
                "Django",
                "JavaScript",
                "React"
            ],
            "certifications": {
                "AWS": "2023-03-12",
                "PMP": "2022-08-30"
            },
            "employee_id": "E12345",
            "employment_date": "2015-09-01"
        }
    elif request.method == 'GET':
        data ={'hai':"hello"}
    return Response(data)

@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method == 'GET':
        obj = Person.objects.all()
        serializer = PersonSerializers(obj,many = True) #many = True is used when serializer expects a queryset or a list of instance (Which means query set expects multiple instance, if many = False then serializer expects a single instance)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializers(obj, data = data, partial = False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializers(obj, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == 'DELETE':
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({'message': "Person deleted successfully"})
