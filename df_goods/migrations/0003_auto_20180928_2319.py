# Generated by Django 2.1 on 2018-09-28 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_auto_20180928_2317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodinfo',
            old_name='goodclick',
            new_name='good_click',
        ),
        migrations.RenameField(
            model_name='goodinfo',
            old_name='goodcontent',
            new_name='good_content',
        ),
        migrations.RenameField(
            model_name='goodinfo',
            old_name='goodimage',
            new_name='good_image',
        ),
        migrations.RenameField(
            model_name='goodinfo',
            old_name='goodintroduce',
            new_name='good_introduce',
        ),
        migrations.RenameField(
            model_name='goodinfo',
            old_name='goodprice',
            new_name='good_price',
        ),
        migrations.RenameField(
            model_name='goodinfo',
            old_name='goodstock',
            new_name='good_stock',
        ),
        migrations.RenameField(
            model_name='goodinfo',
            old_name='goodtitle',
            new_name='good_title',
        ),
        migrations.RenameField(
            model_name='goodinfo',
            old_name='goodtype',
            new_name='good_type',
        ),
        migrations.RenameField(
            model_name='goodinfo',
            old_name='goodunit',
            new_name='good_unit',
        ),
        migrations.RenameField(
            model_name='typeinfo',
            old_name='typetitle',
            new_name='type_title',
        ),
    ]