from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

class UserProfile(models.Model):
    """ LINEユーザーIDなど外部連係情報を保持 """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    line_user_id = models.CharField(max_length=50, unique=True, help_text="LINE Messaging APIのUser ID")

class Plant(models.Model):
    """ 植物情報 """    
    user = models.ForeignKey(get_user_model(), verbose_name='投稿者', on_delete=models.PROTECT)
    name = models.CharField(max_length=100, verbose_name='名前')
    species = models.CharField(max_length=100, verbose_name='種類',blank=True, null=True) # 種類など
    image = models.ImageField(verbose_name='画像',upload_to='plant')
    description = models.TextField(verbose_name='説明',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '植物'
        verbose_name_plural = '植物一覧'

    def __str__(self):
        return self.name

class Work(models.Model):
    """ 植物ごとの作業内容(剪定、施肥、植付け) """    
    WORK_TYPES = (
        ('pruning', '剪定'),
        ('fertilization','施肥'),
        ('planting', '植付け'),
    )

    plant = models.ForeignKey(Plant, verbose_name='植物', on_delete=models.CASCADE)
    work_type = models.CharField(max_length=20, choices=WORK_TYPES, verbose_name='作業名')
    default_interval_days = models.PositiveIntegerField(default=0, verbose_name='作業間隔')
    performed_at = models.DateField(default=timezone.now, verbose_name='作業日')
    notes = models.TextField(blank=True, null=True, verbose_name='作業内容')

    class Meta:
        ordering = ['-performed_at']
        verbose_name = '園芸作業'
        verbose_name_plural = '作業一覧'

    def __str__(self):
        return f"{self.plant.name}-{self.work_type} {self.performed_at}"
        
    @property
    def next_scheduled_date(self):        
        """次回予定日を自動計算"""
        if self.default_interval_days > 0:                  
            return self.performed_at + timedelta(days=self.default_interval_days)
        return None                                  