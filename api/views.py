from rest_framework import viewsets, status
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import  CurrencySerializer , RegistrationSerializer, LoginSerializer, EventSerializer, UserSerializer
from .models import Currency, Event
from .filters import EventFilter


# Create your views here.

def get_cash_register_data():
    # Buy aggregation
    buy_data = Event.objects.filter(type='Buy') \
        .values('currency') \
        .annotate(
            buy_total=Sum('sum'),
            buy_average=ExpressionWrapper(
                Sum(F('price') * F('count')), 
                output_field=DecimalField()
            ) / Sum('count')
        )
    
    # Sell aggregation
    sell_data = Event.objects.filter(type='Sell') \
        .values('currency') \
        .annotate(
            sell_total=Sum('sum'),
            sell_average=ExpressionWrapper(
                Sum(F('price') * F('count')), 
                output_field=DecimalField()
            ) / Sum('count')
        )

    # Combine the results (you can also use `Q` objects for conditional logic)
    combined_data = []
    for buy in buy_data:
        currency = buy['currency']
        sell = next((item for item in sell_data if item['currency'] == currency), None)
        
        if sell:
            # Calculate profit: sell_total * (sell_average - buy_average)
            profit = sell['sell_total'] * (sell['sell_average'] - buy['buy_average'])
        else:
            profit = 0.0
            combined_data.append({
            'currency': currency,
            'buy_total': buy['buy_total'],
            'buy_average': buy['buy_average'],
            'sell_total': sell['sell_total'] if sell else 0.0,
            'sell_average': sell['sell_average'] if sell else 0.0,
            'profit': profit
        })
    
    return combined_data



class CurrencyViewSet(viewsets.ModelViewSet):
    queryset =Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated]


class EventViewSet(viewsets.ModelViewSet):
    queryset =Event.objects.all()
    serializer_class = EventSerializer

    filter_backends = (DjangoFilterBackend,)
    permission_classes = [IsAuthenticated]
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
    def update(self, request, *args, **kwargs):
        event = self.get_object()  # Get the existing event object
        data = request.data
        
        # Extract fields from request data
        price = data.get('price')
        count = data.get('count')
        event_type = data.get('type')
        currency = data.get('currency')
        
        # Ensure price, count, and currency are provided and valid
        if not price or not count or not currency:
            return Response(
                {'detail': 'Price, count, and currency are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate sum based on price and count
        try:
            price = float(price)
            count = float(count)
            sum_value = price * count
        except ValueError:
            return Response(
                {'detail': 'Price and count must be valid numbers.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prepare data for update (sum is automatically calculated)
        updated_data = {
            'price': price,
            'count': count,
            'sum': round(sum_value, 2),
            'type': event_type,
            'currency': currency
        }

        # Update the event fields (excluding sum, as it is auto-calculated)
        for key, value in updated_data.items():
            setattr(event, key, value)

        # Save the updated event object
        event.save()

        # Serialize the updated event and return the response
        serializer = self.get_serializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class LoginView(APIView):
    def post(self,request, *args,**kwargs):
        serializer = LoginSerializer(data =request.data)
        if serializer.is_valid():
             return Response(serializer.save(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UsersView(APIView):
    permission_classes = [IsAuthenticated]
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


class CashRegisterView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        try:
            # Get the cash register data
            data = get_cash_register_data()

            # Return the data as a JSON response
            return Response(data, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Handle any exceptions that occur during data fetching
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ClearAllEventsView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        try:
            # Delete all events
            Event.objects.all().delete()
            return Response({"message": "All events cleared successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)