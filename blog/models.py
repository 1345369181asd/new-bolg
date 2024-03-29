from django.contrib.auth.models import User
from django.db import models


############################ Category:分类
# 1.name:姓名  2.status:状态  3.is_nav:是否导航
# 4.owner:所有者  5.created_time:创建时间
class Category( models.Model ):
    STATUS_NORMAL   = 1
    STATUS_DELETE   = 0
    STATUS_ITEMS    =(
        (STATUS_NORMAL  , '正常'),
        (STATUS_DELETE  , '删除'),
    )
    # 1.name:姓名
    name    = models.CharField( max_length =50, verbose_name = '名称' )
    # 2.status:状态
    status  = models.PositiveIntegerField( default = STATUS_NORMAL ,
                                           choices = STATUS_ITEMS,
                                           verbose_name = '状态'
                                           )
    #is_nav  = models.BooleanField(verbose_name = '是否为导航' )
    #is_nav  = models.BooleanField( defalut = False , verbose_name = '是否为导航' )
    # 3.is_nav:是否导航
    is_nav  = models.BooleanField( default = False , verbose_name = '是否  导航' )
    # 4.owner:所有者
    owner   = models.ForeignKey( User , verbose_name = '作者' , on_delete=models.CASCADE)
    # 5.created_time:创建时间
    created_time = models.DateTimeField( auto_now_add = True , verbose_name = '创建时间' )

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        """
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = categories.filter(is_nav=True)
        normal_categories = categories.filter(is_nav=False)
        """
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        nav_categories = []
        normal_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
            else:
                normal_categories.append(cate)
        return {
            'navs':nav_categories,
            'categories':normal_categories,
        }

############################# Tag:标签
# 1.name:名称  2.status:状态  3.owner:所有者  4.created_time:创建时间
class Tag( models.Model ):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL , '正常' ) ,
        (STATUS_DELETE , '删除' ) ,
    )
    # 1.name:名称
    name = models.CharField( max_length = 10 , verbose_name = '名称' )
    # 2.status:状态
    status = models.PositiveIntegerField(
        default = STATUS_NORMAL ,
        choices = STATUS_ITEMS ,
        verbose_name = '状态'
    )
    # 3.owner:所有者
    owner = models.ForeignKey( User , verbose_name = '作者 ',on_delete=models.CASCADE,)
    # 4.created_time:创建时间
    created_time = models.DateTimeField(
        auto_now_add = True ,
        verbose_name = '创建时间'
    )

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name

############################ Post:文章
# 1.title:标题     2.desc:摘要  3.content:正文  4.status:状态
# 5.category:分类  6.tag:标签   7.ower:所有者   8.created_time:创建时间
class Post( models.Model ):
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL , '正常' ) ,
        (STATUS_DELETE , '删除' ) ,
        (STATUS_DRAFT, '草稿' ) ,
    )
    # 1.title:标题
    title = models.CharField( max_length = 255 , verbose_name = '标题' )
    # 2.desc:摘要
    desc = models.CharField( max_length = 1024 , blank = True , verbose_name = '摘要' )
    # 3.content:正文
    content = models.TextField( verbose_name = '正文' ,help_text = '正文必须为MarkDown格式' )
    # 4.status:状态
    status = models.PositiveIntegerField( default = STATUS_NORMAL ,
                                          choices = STATUS_ITEMS ,
                                          verbose_name = '状态'
                                          )
    # 5.category:分类
    category = models.ForeignKey( Category , verbose_name = '分类',on_delete=models.CASCADE,)
    # 6.tag:标签
    tag = models.ManyToManyField( Tag , verbose_name = '标签' )
    # 7.owner:所有者
    owner = models.ForeignKey( User , verbose_name = '作者',on_delete=models.CASCADE,)
    # 8.created_time:创建时间
    created_time = models.DateTimeField( auto_now_add = True , verbose_name = '创建时间' )

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post_list,tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner', 'category')
        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')