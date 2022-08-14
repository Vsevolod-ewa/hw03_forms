from django.contrib.auth import get_user_model
from django.db import models

from posts.constants import MAX_SHOW_CHAR

User = get_user_model()


class Group(models.Model):
    '''Собирает посты по определенной тематике'''

    title = models.CharField(max_length=200, verbose_name="название")
    slug = models.SlugField(unique=True, verbose_name="номер группы")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title


class Post(models.Model):
    '''Предназначен для публикации постов пользователей'''

    text = models.TextField(max_length=300, verbose_name="текст поста")
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата публикации",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="автор",
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='posts',
        verbose_name="группа",
    )

    class Meta:
        ordering = ('-pub_date', )

    def __str__(self):
        return self.text[:MAX_SHOW_CHAR]
