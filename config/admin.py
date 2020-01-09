from django.contrib import admin

from config.models import Link, SideBar

######################################################################  Link
from typeidea.custom_site import custom_site


@admin.register(Link, site=custom_site)
class LinkAdmin(admin.ModelAdmin):
    # 1.title:标题  2.href:超链接  3.status:状态  4.weight:权重
    # 5.owner:所有者  6.crated_time:创造时间
    # 显示清单
    list_display = ('title','href','status','weight','created_time')
    # fields:字段
    fields = ('title','href','status','weight')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin,self).save_model(request,obj,form,change)



###################################################################### SideBar
@admin.register(SideBar, site=custom_site)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title','display_type','content','created_time')
    fields = ('title','display_type','content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin,self).save_model(request,obj,form,change)

