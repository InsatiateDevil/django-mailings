from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="заголовок")
    text = models.TextField(verbose_name="содержимое статьи")
    image = models.ImageField(verbose_name="изображение")
    view_count = models.PositiveIntegerField(default=0, editable=False, verbose_name="количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")