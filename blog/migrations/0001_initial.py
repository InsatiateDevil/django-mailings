# Generated by Django 4.2.13 on 2024-08-04 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='заголовок')),
                ('text', models.TextField(verbose_name='содержимое статьи')),
                ('image', models.ImageField(upload_to='', verbose_name='изображение')),
                ('view_count', models.PositiveIntegerField(default=0, editable=False, verbose_name='количество просмотров')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
            ],
        ),
    ]