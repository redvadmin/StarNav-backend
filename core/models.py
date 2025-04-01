from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """自定义用户模型"""
    nickname = models.CharField(_('昵称'), max_length=50, blank=True)
    avatar = models.ImageField(_('头像'), upload_to='avatars/', blank=True)
    bio = models.TextField(_('个人简介'), blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = verbose_name
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

class Category(models.Model):
    """导航分类"""
    name = models.CharField('分类名称', max_length=50)
    icon = models.CharField('图标', max_length=50)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '导航分类'
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']

    def __str__(self):
        return self.name

class Navigation(models.Model):
    """导航链接"""
    title = models.CharField('标题', max_length=100)
    url = models.URLField('链接')
    icon = models.CharField('图标', max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='所属分类')
    description = models.TextField('描述', blank=True)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '导航链接'
        verbose_name_plural = verbose_name
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

class UserNote(models.Model):
    """用户笔记"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    content = models.TextField('内容')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户笔记'
        verbose_name_plural = verbose_name
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username}的笔记 - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

class UserSettings(models.Model):
    """用户设置"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    theme = models.CharField('主题', max_length=20, default='light')
    layout = models.CharField('布局', max_length=20, default='grid')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户设置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}的设置"
