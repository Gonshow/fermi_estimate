from django.db import models


class Post(models.Model):
    title = models.CharField('記事タイトル', max_length=255)
    text = models.TextField('記事本文')

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('コメント内容')
    post = models.ForeignKey(Post, verbose_name='対象記事', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='親コメント', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:10]
