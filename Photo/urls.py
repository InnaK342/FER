from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('photo_form/', photo_form, name='photo_form'),
    path('person_page/<int:user_id>/', person_page, name='person_page'),
    path('photo_delete/<int:photo_id>/', delete_photo, name='delete_photo'),
]