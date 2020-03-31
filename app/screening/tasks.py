from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery_progress.backend import ProgressRecorder
import time
from datetime import datetime
from django.utils import timezone
import pandas as pd
from io import StringIO
from screening.models import PubmedImport
from screening.utils.pubmedimporter import pubmedid_import

@shared_task(bind=True)
def import_pubmedids(self, pmids, search_function):
    progress_recorder = ProgressRecorder(self)
    result = 0

    import_record = PubmedImport()
    import_record.import_date = timezone.now()
    import_record.search_function = search_function
    import_record.save()
    import_id = import_record.id

    pmids_io = StringIO(pmids)
    df = pd.read_csv(pmids_io, header=None)

    for index, record in df.iterrows():
        pmid = record[0]
        print('importing {0}'.format(pmid))

        pubmedid_import(pmid, import_record)

        progress_recorder.set_progress(index, df.shape[0])

    return df.shape[0]
