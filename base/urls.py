from django.urls import path 

from . import views  

urlpatterns=[

    path('',views.home,name="home"),
    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutuser,name="logout"),
    path('profile/<str:pk>/',views.userprofile,name="user-profile"),
    path('register/',views.registeruser,name="register"),
    path('room/<str:pk>/',views.room,name="room"),
    path('create-room',views.createRoom,name="create-room"),
    path('update-room/<str:pk>/',views.UpdateRoom,name="update-room"),
    path('delete-room/<str:pk>/',views.delRoom,name="delete-room"),
    path('delete-message/<str:pk>/',views.delmessage,name="delete-message"),
    path('topics',views.topicspage,name="topics"),
    path('activiity',views.activitypage,name="activity"),
    path('update-user/',views.updateuser,name="update-user"),


]