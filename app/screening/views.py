from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from random import randint
from haystack.utils.highlighting import Highlighter
from screening.utils.highlighter import LitrevHighlighter


def __highlight_text(text, highlights, css_class):
    keywords = list()
    [keywords.append(h.text) for h in highlights]
    query = ' '.join(keywords)
    highlighter = LitrevHighlighter(query, css_class=css_class, max_length=10000)
    return highlighter.highlight(text)

def index(request):
    articles = PubmedImportedArticle.objects.filter(screened=False)

    if len(articles) <= 0:

        return render(request, 'screening/empty.html')

    idx = randint(0, len(articles)-1)
    article = articles[idx]

    highlights_green = Highlight.objects.filter(highlight_type='I')
    highlights_red = Highlight.objects.filter(highlight_type='E')

    article.abstract = __highlight_text(article.abstract, highlights_green, "bg-success text-white")
    article.abstract = __highlight_text(article.abstract, highlights_red, "bg-danger text-white")
    article.abstract = article.abstract[1:]
    article.abstract = article.abstract[:-1]

    article.title = __highlight_text(article.title, highlights_green, "bg-success text-white")
    article.title = __highlight_text(article.title, highlights_red, "bg-danger text-white")

    articles_screened = PubmedImportedArticle.objects.filter(screened=True)
    articles_total = len(articles) + len(articles_screened)
    progress = int((len(articles_screened)/articles_total) * 100)

    data = {
        "article": article,
        "articles_screened": len(articles_screened),
        "progress": progress,
        "articles_total": articles_total
    }

    return render(request, 'screening/index.html', data)

def process_article(request, id=0, action=''):
    if action == 'maybe':
        pass
    else:
        article = PubmedImportedArticle.objects.get(pk=id)
        article.screened = True
        article_status = ScreeningStatus()
        article_status.article = article

        if action == 'accept':
            article_status.decision = 'Y'
        elif action == 'reject':
            article_status.decision = 'N'

        article.save()
        article_status.save()

    return redirect('screening:index')
