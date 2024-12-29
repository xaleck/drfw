from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import  ArticleSerializer , RegistrationSerializer, LoginSerializer
from .models import Article


# Create your views here.


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data =request.data)
        if serializer.is_valid() :
            user = serializer.save()

            return Response( {"message": "User registered successfully",
                "user": {
                    "username": user.username,
                    "email": user.email,
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self,request, *args,**kwargs):
        serializer = LoginSerializer(data =request.data)
        if serializer.is_valid():
             return Response(serializer.save(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)