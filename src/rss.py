import requests
import xmltodict
import shared_functions
from flask import Blueprint

rss = Blueprint('rss', __name__)

@rss.route('/rss/<feed>')
def renderFeed(feed):
    feedurls=shared_functions.config['feed_urls']
    rss_xml = requests.get(feedurls[feed])
    html_return = []
    rss_dict = xmltodict.parse(rss_xml.text)
    if "rss" in rss_dict.keys():
        rss_dict = rss_dict["rss"]
        items = rss_dict["channel"]['item']
    elif "rdf:RDF" in rss_dict.keys():
        rss_dict = rss_dict['rdf:RDF']
        items = rss_dict["item"]
    html_return.append("<h2>" + rss_dict["channel"]['title'] + "</h2>")
    try:
        html_return.append("<h5>" + rss_dict["channel"]['description'] + "</h5>")
    except:
        print("Unasble to get channel description.")
    if "image" in rss_dict["channel"].keys():
        if "url" in rss_dict["channel"]["image"].keys():
            html_return.append(shared_functions.saveImageToCache(rss_dict["channel"]['image']['url']))
        elif "@rdf:resource" in rss_dict["channel"]["image"].keys():
            html_return.append(shared_functions.saveImageToCache(rss_dict["channel"]['image']['@rdf:resource']))
    for item in items:
        html_return.append('<hr>')
        html_return.append('<h4>' + item['title'] + "</h4>")
        html = item['description']
        if "content:encoded" in item.keys():
            html = item['content:encoded']
        html_return.append(shared_functions.parseHTML(html))
        if "media:group" in item.keys():
            img = item['media:group']['media:content'][0]
            html_return.append(shared_functions.saveImageToCache(img['@url']))
        if "image" in item.keys():
            html_return.append(shared_functions.saveImageToCache(item['image']))
        if "enclosure" in item.keys():
            html_return.append(shared_functions.saveImageToCache(item['enclosure']['@url']))
        if "link" in item.keys():
            html_return.append('<a href="/htmlscraper/' + item['link'] + '">Read More</a>')

    html = "\n".join(html_return)
    return html