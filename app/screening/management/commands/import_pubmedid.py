import os
import numpy as np
from datetime import datetime
import pytz
from pubmed_lookup import PubMedLookup, Publication
from django.core.management.base import BaseCommand
from django.utils import timezone
from screening.models import PubmedImport, PubmedImportedArticle

class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('-p', '--pmid', type=str, help='Pubmed id')

    def get_int(self, number):
        result = 1
        try:
            result = int(number)
        except (TypeError, ValueError):
            result = 1
        return result

    def handle(self, *args, **options):
        print('importing {0}'.format(options['pmid']))

        pmid = options['pmid']

        import_record = PubmedImport()
        import_record.import_date = timezone.now()
        import_record.search_function = pmid
        import_record.save()
        import_id = import_record.id

        find_pmid = PubmedImportedArticle.objects.filter(pmid=pmid)
        if len(find_pmid) > 0:
            print('{0} already exists'.format(pmid))
        else:
            try:
                email = ''
                url = 'http://www.ncbi.nlm.nih.gov/pubmed/{0}'.format(pmid)
                lookup = PubMedLookup(url, email)
                publication = Publication(lookup, resolve_doi=False)
                pia = PubmedImportedArticle()
                pia.pmid = pmid
                year = self.get_int(publication.year)
                month = self.get_int(publication.month)
                day = self.get_int(publication.day)
                pia.pub_date = datetime(year, month, day, 0, 0, 0, 0, tzinfo=pytz.UTC)
                pia.title = publication.title
                pia.authors = publication.authors
                pia.journal = publication.journal
                pia.citation = publication.cite()
                # pia.mini_citation = publication.cite_mini()
                pia.url = publication.url
                pia.pubmed_url = publication.pubmed_url
                pia.abstract = repr(publication.abstract)
                pia.screened = False
                pia.tagged = False
                pia.landmark = False
                pia.pmimport = import_record
                pia.save()
            except:
                print('\nPMID {0} failed'.format(pmid))

        print('finished')
