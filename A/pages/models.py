from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام')
    sub_category = models.ForeignKey('self', models.CASCADE, related_name='scategory', null=True, blank=True,
                                     verbose_name='زیر دسته')
    is_sub_category = models.BooleanField(default=False, verbose_name='آیا زیر دسته است؟')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pages:category_slug', args=[self.slug])
