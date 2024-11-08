from django.contrib import admin
from .models import TrashCan, TrashCompartment, Trash

# Đăng ký mô hình TrashCan
class TrashCanAdmin(admin.ModelAdmin):
    list_display = ('id', 'position') 
    search_fields = ('position',)      

# Đăng ký mô hình TrashCompartment
class TrashCompartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_trash_can', 'empty_count', 'label', 'max_quantity')  
    list_filter = ('id_trash_can',)     
    search_fields = ('label',)

# Đăng ký mô hình Trash
class TrashAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_trash_can', 'id_trash_compartment', 'trash_img_url', 'trash_img_public_id', 'date', 'quantity')  
    list_filter = ('date', 'id_trash_compartment')  
    search_fields = ('trash_img_url',)  

# Đăng ký các mô hình với Django Admin
admin.site.register(TrashCan, TrashCanAdmin)
admin.site.register(TrashCompartment, TrashCompartmentAdmin)
admin.site.register(Trash, TrashAdmin)
