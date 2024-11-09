from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('api/login', views.login, name='login'),
    path('api/logout', views.logout, name='logout'), 
    path('api/upload-image', views.uploadImage, name='uploadImage'),
    path('api/trash-data/<int:trash_area_id>', views.getTrashData, name='getTrashData'), 
    path('api/trash-area-progress/<int:trash_area_id>', views.getTrashProgess, name='getTrashProgess'), 
    path('api/reset-progress/<int:trash_compartment_id>', views.resetProgress, name='resetProgress'), 
    path('api/get-trash-data-to-chart/<int:trash_area_id>', views.getTrashDataToChart, name='getTrashDataToChart'),
    path('api/get-trash-area-data-for-esp32/<int:trash_area_id>', views.getTrashAreaDataForEsp32, name='getTrashAreaDataForEsp32'), 
]   