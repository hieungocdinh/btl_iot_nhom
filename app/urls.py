from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'), 
    path('api/upload-image', views.uploadImage, name='uploadImage'),
    path('api/trash-data/<int:trash_can_id>', views.getTrashData, name='getTrashData'), 
    path('api/trash-can-progress/<int:trash_can_id>', views.getTrashProgess, name='getTrashProgess'), 
    path('api/reset-progress/<int:trash_compartment_id>', views.resetProgress, name='resetProgress'), 
    path('api/get-trash-data-to-chart/<int:trash_can_id>', views.getTrashDataToChart, name='getTrashDataToChart'), 
]   