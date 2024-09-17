from django.urls import path
from .views import *

urlpatterns = [
    path('machine', MachineCRUDOperation.as_view()),
    path('machine/<int:id>', MachineCRUDOperation.as_view()),
    path('axis', AxisCRUDOperation.as_view()),
    path('axis/<int:id>', AxisCRUDOperation.as_view()),
    # path('login', Login.as_view()),
]