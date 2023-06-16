from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Plant(models.Model):
    class Meta:
        verbose_name_plural = '植物'
        
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    name = models.CharField(verbose_name='名前', max_length=30)
    text = models.TextField(verbose_name='内容')    
    uetuke_date = models.DateField(verbose_name='植付月日等', default=timezone.now)
    image = models.ImageField(verbose_name='イメージ', upload_to='image/', blank=True, null=True)
    categories = models.ManyToManyField(
        'Category',
        verbose_name = 'カテゴリ',
        blank=True,
        related_name='plants',
    )

              
class Category(models.Model):
    name = models.CharField(max_length=1024)
    slug = models.CharField(max_length=1024)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name