from django.contrib import admin

from comment.models import Comment

############################Comment
from typeidea.custom_site import custom_site


@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    # target:目标  content:内容  nickname:昵称  website:网站
    # email:邮箱  status:状态  created_time:创建时间
    list_display = ('target','nickname','content','website','created_time')