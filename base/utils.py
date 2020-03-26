import csv
import xml.etree.ElementTree as ET
from django.http import HttpResponse


def build_csv_response(col_names, data, filename='export.csv'):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename ="{0}"'.format(filename)
    writer = csv.writer(response)

    writer.writerow(col_names)

    for dat in data:
        writer.writerow(dat)

    return response

def build_mendeley_xml_response(data, filename='export.xml'):
    xml_data = ET.Element('xml')
    records = ET.SubElement(xml_data, 'records')

    for d in data:
        record = ET.SubElement(records, 'record')

        accession_num = ET.SubElement(record, 'accession-num')
        accession_num.text = d['pmid']
        titles = ET.SubElement(record, 'titles')
        title = ET.SubElement(titles, 'title')
        title.text = d['title']
        label = ET.SubElement(record, 'label')
        label.text = d['tags']
        rev_type = ET.SubElement(record, 'ref-type')
        rev_type.set('name', 'Journal Article')
        rev_type.text = 0

    # create a new XML file with the results
    data_str = ET.tostring(xml_data)
    print(data_str)

    response = HttpResponse(content_type='text/xml')
    response['Content-Disposition'] = 'attachment; filename ="{0}"'.format(filename)
    response.write(data_str)
    return response
