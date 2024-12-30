from rest_framework import viewsets, status
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import  CurrencySerializer , RegistrationSerializer, LoginSerializer, EventSerializer, UserSerializer
from .models import Currency, Event
from .filters import EventFilter


# Create your views here.




class CurrencyViewSet(viewsets.ModelViewSet):
    queryset =Currency.objects.all()
    serializer_class = CurrencySerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset =Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventFilter  # Use the filter class we just created

    # Optionally, you can override the `get_queryset` method to handle custom filtering logic:
    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter events by currency and type if provided in the query parameters
        currency = self.request.query_params.get('currency', None)
        event_type = self.request.query_params.get('type', None)

        if currency:
            queryset = queryset.filter(currency__iexact=currency)
        if event_type:
            queryset = queryset.filter(type__iexact=event_type)

        return queryset

    
class LoginView(APIView):
    def post(self,request, *args,**kwargs):
        serializer = LoginSerializer(data =request.data)
        if serializer.is_valid():
             return Response(serializer.save(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UsersView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all() 
        user_serializer = UserSerializer(users, many=True)

        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data =request.data)
        if serializer.is_valid() :
            user = serializer.save()

            return Response( {"message": "User registered successfully",
                "user": {
                    "username": user.username,
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        # Get the user id from the URL
        user_id = kwargs.get('id')
        
        try:
            # Try to get the user object by the given id
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": f"User with id {user_id} deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        
        except User.DoesNotExist:
            # Return a 404 error if the user doesn't exist
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)