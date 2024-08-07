from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="заголовок")
    text = models.TextField(verbose_name="содержимое статьи")
    image = models.ImageField(upload_to='blog/', verbose_name="изображение", blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0, editable=False, verbose_name="количество просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
