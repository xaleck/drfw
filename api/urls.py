from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrencyViewSet, RegisterView, LoginView, EventViewSet

router = DefaultRouter()

router.register(r'currency', CurrencyViewSet)
router.register(r'events', EventViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name = 'login'),
]