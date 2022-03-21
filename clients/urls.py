from django.urls import path
from .views import ClientGenericAPIView

urlpatterns = [
    path('clients', ClientGenericAPIView.as_view()),
    path('clients/<str:pk>', ClientGenericAPIView.as_view()),
]