
from django.urls import path
from .views import register, home_page, Class_Detail, enroll_class, login_view, \
     enroll_class, enrolled_class_list


urlpatterns = [

    path('register/', register, name='register'),
    path('', home_page, name='home'),
    path('class_detail/<int:pk>/', Class_Detail.as_view(), name='class_detail'),
    path('enroll_class/<int:pk>/', enroll_class, name='enroll_class'),
    path('login/', login_view, name='login'),
    path('enroll_class/', enroll_class, name='enroll_class'),
    path('enrolled_class_list/', enrolled_class_list, name='enrolled_class_list'),
]
