from django.db import models
from django.urls import reverse_lazy

class Post(models.Model):
    title = models.CharField('推定テーマ', max_length=255)
    text = models.TextField('記事本文')
    formula = models.CharField(verbose_name="モデル式", max_length=255, blank=True, null=True)
    formula_out = models.CharField(verbose_name="表示用式", max_length=255, blank=True, null=True)
    value = models.FloatField(verbose_name='結果', blank=True, null=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse_lazy("blog:post_detail", args=[self.id])

class Comment(models.Model):
    text = models.TextField('因子名')
    sub_name = models.CharField(verbose_name="変数名", max_length=255, blank=True, null=True)
    depth = models.IntegerField(verbose_name='深さ', default=0, blank=True, null=True)
    value = models.FloatField(verbose_name='数値', blank=True, null=True)
    formula = models.CharField(verbose_name="モデル式", max_length=255, blank=True, null=True)
    post = models.ForeignKey(Post, verbose_name='対象記事', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='親コメント', null=True, blank=True, on_delete=models.CASCADE)
    formula_out = models.CharField(verbose_name="表示用式", max_length=255, blank=True, null=True)
    def __str__(self):
        return self.text
