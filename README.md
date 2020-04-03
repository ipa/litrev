![Django CI](https://github.com/ipa/litrev/workflows/Django%20CI/badge.svg) ![Docker](https://github.com/ipa/litrev/workflows/Docker/badge.svg)

# Literature Review

Quick and dirty database for literature review:

* Import PubMed search
* Screen for relevant articles
* Add tags to articles
* Export articles and tags to Mendeley

## Pubmed import

python manage.py import_from_pubmed --path "pubmed_result.csv" --search_function "search_function.txt"
