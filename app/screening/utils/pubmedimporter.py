from screening.models import PubmedImport, PubmedImportedArticle
from pubmed_lookup import PubMedLookup, Publication
from django.utils import timezone
from datetime import datetime
import sys
import pytz


def get_int(number):
    result = 1
    try:
        result = int(number)
    except (TypeError, ValueError):
        result = 1
    return result

def pubmedid_import(pmid, import_record):
    find_pmid = PubmedImportedArticle.objects.filter(pmid=pmid)
    if len(find_pmid) > 0:
        return

    try:
        email = ''
        url = 'http://www.ncbi.nlm.nih.gov/pubmed/{0}'.format(get_int(pmid))
        lookup = PubMedLookup(url, email)
        publication = Publication(lookup, resolve_doi=False)
        pia = PubmedImportedArticle()
        pia.pmid = pmid
        year = get_int(publication.year)
        month = get_int(publication.month)
        day = get_int(publication.day)
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
        print("Unexpected error:", sys.exc_info())
        # failed_ids.append(pmid)
        # np.savetxt('failed_ids.txt', np.asarray(failed_ids), fmt='%d')
