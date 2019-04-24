from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.home, name='home'),
    path('submit/', views.submit , name='submit'),
    path('submit/thanks/', views.thanks, name='thanks'),
    path('sms',views.sms,name='sms'),
    path('login/',views.loginid, name='login'),
    path('data/',views.view_data,name='data'),
    path('register/',views.register,name='register'),
    path('chat/',views.chat,name='chatfeature')

]