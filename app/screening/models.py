from django.db import models

# Create your models here.

class PubmedImport(models.Model):
    import_date = models.DateTimeField('date imported')
    search_function = models.TextField()

class PubmedImportedArticle(models.Model):
    pmimport = models.ForeignKey(PubmedImport, on_delete=models.PROTECT)
    pmid = models.CharField(max_length=15)
    pub_date = models.DateTimeField('date published')
    title = models.CharField(max_length = 300)
    authors = models.CharField(max_length = 500)
    journal = models.CharField(max_length = 200)
    citation = models.CharField(max_length = 500)
    mini_citation = models.CharField(max_length = 500)
    url = models.CharField(max_length = 250)
    pubmed_url = models.CharField(max_length = 250)
    abstract = models.TextField()
    screened = models.BooleanField()
    tagged = models.BooleanField()
    landmark = models.BooleanField()

    def __str__(self):
        return self.title


HIGHLIGHT_TYPE = (
            ('E','Exclude'),
            ('I','Include'),
            )

class Highlight(models.Model):
    text = models.CharField(max_length = 50)
    highlight_type = models.CharField(choices=HIGHLIGHT_TYPE, max_length=1)

SCREENING_DECISION = (
    ('N', 'No'),
    ('Y', 'Yes'),
    ('U', 'Unclear')
)

class ScreeningStatus(models.Model):
    article = models.ForeignKey(PubmedImportedArticle, on_delete=models.PROTECT)
    decision = models.CharField(choices=SCREENING_DECISION, max_length=1)
