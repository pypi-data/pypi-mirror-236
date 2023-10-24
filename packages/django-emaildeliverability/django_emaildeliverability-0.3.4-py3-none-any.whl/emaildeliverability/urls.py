from django.urls import path
from emaildeliverability import views

urlpatterns = [
    path('check/', views.emaildeliverability)
]