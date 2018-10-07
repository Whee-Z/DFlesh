from django.db import models
from tinymce.models import HTMLField

# Create your models here.
#商品分类
class TypeInfo(models.Model):
    type_title = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.type_title

#商品类
class GoodInfo(models.Model):
    good_title = models.CharField(max_length=20)
    good_image = models.ImageField(upload_to='df_goods')
    good_price = models.DecimalField(max_digits=5,decimal_places=2)
    isDelete = models.BooleanField(default=False)
    #单位
    good_unit = models.CharField(max_length=20,default='500g')
    #点击量，用于排序呈现出来
    good_click = models.IntegerField()
    #简介
    good_introduce = models.CharField(max_length=200)
    #库存
    good_stock = models.IntegerField()
    #详细简介内容
    good_content = HTMLField()
    #引用外键
    good_type = models.ForeignKey(TypeInfo,on_delete=models.CASCADE)

    def __str__(self):
        return self.good_title