import requests
import shared_functions
from urllib.parse import urlparse
from flask import Blueprint

htmlparser = Blueprint('htmlparser', __name__)


@htmlparser.route('/htmlscraper/<path:url>')
def scrapewebpage(url):
    if '://' not in url:
        url = url.replace(":/","://")
    parsed_url = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_url)
    protocol = url.split(':')[0]
    html = requests.get(url).content
    if "www.kwqc.com" in url:
        return shared_functions.parseHTML(html, metaimg=True, domain=domain, protocol=protocol)
    return shared_functions.parseHTML(html, domain=domain, protocol=protocol)