from . import views
from django.urls import path
from .views import CreateProfilePageView
urlpatterns = [
    path('',views.home, name='home'),
    path('room/<int:id>/',views.room, name='room'),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<int:id>/',views.updateRoom,name='update-room'),
    path('delete-room/<int:id>/',views.deleteRoom,name='delete-room'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerUser,name='register'),
    path('update-user/',views.updateUser,name='update-user'),
    path('delete-message/<int:id>/',views.deleteMessage,name='delete-message'),
    path('profile/<int:id>/',views.userProfile,name='userprofile'),
    path('create-user/',CreateProfilePageView.as_view(),name='create-user')
]