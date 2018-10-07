from django.contrib import admin
from .models import *

# Register your models here.
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id','type_title']

class GoodInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id','good_title','good_image','good_price','good_unit','good_stock','good_content','good_type']

admin.site.register(TypeInfo,TypeInfoAdmin)
admin.site.register(GoodInfo,GoodInfoAdmin)
