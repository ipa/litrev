from django.db import models
from screening.models import PubmedImportedArticle
# Create your models here.

class TagGroup(models.Model):
    group_name = models.CharField(max_length = 25)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return '{0}'.format(self.group_name)

class Tag(models.Model):
    tag_name = models.CharField(max_length = 25)
    tag_group = models.ForeignKey(TagGroup, on_delete=models.PROTECT)
    tagged = False

    def __str__(self):
        return '{0} ({1})'.format(self.tag_name, self.id)


class ArticleTag(models.Model):
    article = models.ForeignKey(PubmedImportedArticle, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)

class Highlight(models.Model):
    keyword = models.CharField(max_length = 30)
    css_class = models.CharField(max_length = 30)
