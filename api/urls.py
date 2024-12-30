from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import CurrencyViewSet, LoginView, EventViewSet, UsersView,CashRegisterView,ClearAllEventsView

router = DefaultRouter()

router.register(r'currency', CurrencyViewSet)
router.register(r'events', EventViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name = 'login'),
    path('users/', UsersView.as_view(), name='users'),
    path('delete-user/<int:id>/', UsersView.as_view(), name='delete-user'),
     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('cash_register/', CashRegisterView.as_view(), name='cash_register'),
     path('clear-all-events/', ClearAllEventsView.as_view(), name='clear-all-events'),
    
]