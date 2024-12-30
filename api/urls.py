from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrencyViewSet, LoginView, EventViewSet, UsersView,CashRegisterView

router = DefaultRouter()

router.register(r'currency', CurrencyViewSet)
router.register(r'events', EventViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name = 'login'),
    path('users/', UsersView.as_view(), name='users'),
    path('delete-user/<int:id>/', UsersView.as_view(), name='delete-user'),
    path('cash_register/', CashRegisterView.as_view(), name='cash_register')
]