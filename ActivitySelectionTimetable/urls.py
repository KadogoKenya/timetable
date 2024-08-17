
from django.contrib import admin
from django.urls import path, include
import ActivitySelectionTimetable.settings
from django.urls import re_path
from timetableapp import views
from django.contrib.auth.views import LoginView,LogoutView



urlpatterns = [
    # path('admin/', admin.site.urls),

    path('admin/', admin.site.urls, name='admin'),
    re_path('accounts/',include('django.contrib.auth.urls') ),
    
    
    re_path('accounts/', include('django.contrib.auth.urls')),
    re_path('adminsignup_view', views.adminsignup_view),
    re_path('adminlogin', LoginView.as_view(template_name='timetableapp/adminlogin.html')),
    re_path('afterlogin', views.afterlogin_view),
    
    re_path('login/', views.login, name="login"),
    re_path('afterlogin', views.afterlogin_view),
    re_path('studentsignup', views.studentsignup_view),
    re_path('studentclick', views.studentclick_view),    
    re_path('studentlogin', LoginView.as_view(template_name='timetable/studentlogin.html')),

    re_path('logout', LogoutView.as_view(template_name='timetable/course_list.html')),
    

   

    re_path('adminsignup_view', views.adminsignup_view),
    re_path('adminlogin', LoginView.as_view(template_name='timetableapp/adminlogin.html')),

    re_path('afterlogin', views.afterlogin_view),
    
    
    re_path('login/', views.login, name="login"),
    re_path('afterlogin', views.afterlogin_view),
    re_path('studentsignup', views.studentsignup_view),
    re_path('studentclick', views.studentclick_view),    
    re_path('studentlogin', LoginView.as_view(template_name='timetable/studentlogin.html')),


    re_path('lecturersignup', views.lecturersignup_view),
    re_path('lecturerlogin', LoginView.as_view(template_name='timetableapp/lecturerlogin.html')),

    re_path('logout', LogoutView.as_view(template_name='timetable/course_list.html')),

    re_path('',include('timetableapp.urls')),

]
