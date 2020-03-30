from .models import *
from screening.models import ScreeningStatus, PubmedImportedArticle
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from random import randint
from screening.utils.highlighter import LitrevHighlighter
import numpy as np
from .forms import LandmarkPaperForm

from base.utils import build_csv_response, build_mendeley_xml_response

def __highlight_text(text, highlights, css_class):
    # keywords = list()
    # [keywords.append(h.text) for h in highlights]
    # query = ' '.join(highlights)
    highlighter = LitrevHighlighter(highlights, css_class=css_class, max_length=10000)
    return highlighter.highlight(text)

def index(request, id=-1):
    if id is not -1:
        article = ScreeningStatus.objects.get(article_id=id)
    else:
        included_articles = ScreeningStatus.objects.filter(decision='Y', article__tagged=False)

        if len(included_articles) <= 0:
            return render(request, 'tagging/empty.html')

        idx = randint(0, len(included_articles)-1)
        article = included_articles[idx]

    highlights = Highlight.objects.all()
    for h in highlights.iterator():
        article.article.abstract = __highlight_text(article.article.abstract, h.keyword, h.css_class)
        article.article.title = __highlight_text(article.article.title, h.keyword, h.css_class)

    article.article.abstract = article.article.abstract[1:]
    article.article.abstract = article.article.abstract[:-1]

    tags = Tag.objects.all()
    tag_group = TagGroup.objects.filter(enabled=True)

    available_tags = list()

    for tg in tag_group:
        tags_in_group = tg.tag_set.all()
        group_tags = {
            'group_name': tg.group_name,
            'tags': list()
        }
        for t in tags_in_group:
            article_tags = ArticleTag.objects.filter(article_id = article.article_id, tag_id = t.id)
            group_tags['tags'].append({
                'tag_id': t.id,
                'tag_name': t.tag_name,
                'tagged': len(article_tags) > 0
            })
        available_tags.append(group_tags)

    tagged_articles = ArticleTag.objects.values_list('article_id')

    num_tagged_articles = np.count_nonzero(np.unique(np.array(tagged_articles)))
    num_articles = ScreeningStatus.objects.filter(decision='Y').count()
    progress = int((num_tagged_articles / num_articles) * 100)

    data = {
        'article': article.article,
        'tags': tags,
        'available_tags': available_tags,
        'progress': progress,
        'articles_total': num_articles,
        'articles_tagged': num_tagged_articles
    }

    return render(request, 'tagging/index.html', data)


def view_tags(request, article_id=0):
    # tagged_articles = PubmedImportedArticle.objects.filter(tagged=True).order_by('pmid')
    # article = tagged_articles[article_id]
    article = PubmedImportedArticle.objects.get(pmid=article_id)

    tags = ArticleTag.objects.filter(article_id = article.id)

    data = {
        'article': article,
        'tags': tags,
        'next_idx': article_id + 1,
        'prev_idx': article_id - 1
        # 'available_tags': available_tags,
        # 'progress': progress,
        # 'articles_total': num_articles,
        # 'articles_tagged': num_tagged_articles
    }

    return render(request, 'tagging/view_tags.html', data)


def landmark_papers(request):
    tagged_articles = PubmedImportedArticle.objects.filter(landmark=True).order_by('pmid')

    if request.method == 'POST':
        form = LandmarkPaperForm(request.POST)
        if form.is_valid():
            pmid = form.cleaned_data['pmid']
            print(pmid)
            article = PubmedImportedArticle.objects.get(pmid=pmid)
            print(article)
            article.landmark = True
            article.save()



    form = LandmarkPaperForm()

    data = {
        'articles': tagged_articles,
        'form': form
    }

    return render(request, 'tagging/landmark_papers.html', data)

def tag_article(request, article_id=0, tag_id=0):
    article = PubmedImportedArticle.objects.get(pk=article_id)
    tag = Tag.objects.get(pk=tag_id)

    article_tags = ArticleTag.objects.filter(article_id = article_id, tag_id = tag_id)
    if len(article_tags) == 1:
        article_tags.delete()
    else:
        article_tag = ArticleTag()
        article_tag.article = article
        article_tag.tag = tag
        article_tag.save()

    article_tags = ArticleTag.objects.filter(article_id = article_id)
    if len(article_tags) > 0:
        article.tagged = True
        article.save()

    return redirect('tagging:index', id=article_id)

def mark_irrelevant(request, article_id=0):
    article_status = ScreeningStatus.objects.get(article_id=article_id)
    article_status.decision = 'N'
    article_status.save()

    return redirect('tagging:index')

def export(request):
    return render(request, 'tagging/export.html')

def export_csv(request):
    tagged_articles = PubmedImportedArticle.objects.filter(tagged=True)

    col_names = ['PMID', 'authors', 'year', 'month', 'title', 'tags']
    data = []
    for ta in tagged_articles:
        tags = []
        [tags.append(t.tag.tag_name) for t in ta.articletag_set.all()]
        tags_str = ','.join(tags)
        data.append([ta.pmid, ta.authors, ta.pub_date.year, ta.pub_date.month, ta.title, tags_str])
    return build_csv_response(col_names, data)


def export_landmarks_csv(request):
    tagged_articles = PubmedImportedArticle.objects.filter(landmark=True)

    col_names = ['PMID', 'authors', 'authors_etal', 'year', 'month', 'title', 'tags']
    data = []
    for ta in tagged_articles:
        tags = []
        [tags.append(t.tag.tag_name) for t in ta.articletag_set.all()]
        tags_str = ','.join(tags)
        authors_etal = ta.authors.split()[0] + " et al."
        data.append([ta.pmid, ta.authors, authors_etal, ta.pub_date.year, ta.pub_date.month, ta.title, tags_str])
    return build_csv_response(col_names, data, filename='soa-timeline.csv')


def export_mendeley(request):
    tagged_articles = PubmedImportedArticle.objects.filter(tagged=True)

    data = []
    for ta in tagged_articles:
        tags = []
        [tags.append(t.tag.tag_name) for t in ta.articletag_set.all()]
        tags_str = ';'.join(tags)
        data.append({
            'pmid': ta.pmid,
            'title': ta.title,
            'tags': tags_str
        })
    return build_mendeley_xml_response(data)
