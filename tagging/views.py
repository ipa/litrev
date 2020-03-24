from .models import *
from screening.models import ScreeningStatus, PubmedImportedArticle, Highlight
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from random import randint
from screening.utils.highlighter import LitrevHighlighter
import numpy as np

from base.utils import build_csv_response, build_mendeley_xml_response

def __highlight_text(text, highlights, css_class):
    keywords = list()
    [keywords.append(h.text) for h in highlights]
    query = ' '.join(keywords)
    highlighter = LitrevHighlighter(query, css_class=css_class, max_length=10000)
    return highlighter.highlight(text)

def index(request, id=-1):
    print(id)
    if id is not -1:
        article = ScreeningStatus.objects.get(article_id=id)
    else:
        included_articles = ScreeningStatus.objects.filter(decision='Y', article__tagged=False)

        idx = randint(0, len(included_articles)-1)
        article = included_articles[idx]

    highlights_green = Highlight.objects.filter(highlight_type='I')
    article.article.abstract = __highlight_text(article.article.abstract, highlights_green, "bg-success text-white")
    article.article.abstract = article.article.abstract[1:]
    article.article.abstract = article.article.abstract[:-1]

    article.article.title = __highlight_text(article.article.title, highlights_green, "bg-success text-white")

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

    return redirect('tagging:index', id=article_id)

def export(request):
    return render(request, 'tagging/export.html')

def export_csv(request):
    tagged_articles = PubmedImportedArticle.objects.filter(tagged=True)

    col_names = ['PMID', 'title', 'tags']
    data = []
    for ta in tagged_articles:
        tags = []
        [tags.append(t.tag.tag_name) for t in ta.articletag_set.all()]
        tags_str = ','.join(tags)
        data.append([ta.pmid, ta.title, tags_str])
    return build_csv_response(col_names, data)


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


# def exp_export_csv(request):
#     experiments = Experiment.objects.filter(exclude_from_analysis=False)
#
#     col_names = ['date', 'profile_id', 'result_length', 'result_width', 'result_area', 'specimen_temperature', 'room_temperature',
#                  'average_delivered_power', 'delivered_energy', 'ablation_device', 'specimen_id']
#
#     data = []
#     for ex in experiments:
#         data.append([ex.exp_date, ex.profile.id, ex.result_length, ex.result_width, ex.result_area, ex.specimen_temperature,
#                      ex.room_temperature, ex.average_delivered_power, ex.delivered_energy, ex.ablation_device, ex.specimen.id])
#
#     return utils.build_csv_response(col_names, data)
