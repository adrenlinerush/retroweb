import requests
import shutil
from PIL import Image
from bs4 import BeautifulSoup
import configparser

config=configparser.ConfigParser()
config.read('config.ini')

def saveImageToCache(imgUrl, resize=True, new_h=300):
    try:
        filename = imgUrl.split("/")[-1]
        if 'twitter' in filename.lower() \
           or 'skipme' in filename.lower() \
           or 'marketpulse' in filename.lower() \
           or 'realtimeheadlines' in filename.lower() \
           or 'topstories' in filename.lower():
            return ''
        img = requests.get(imgUrl, stream = True)
        suffix = filename[-3:].lower()
        if "DualImage" in filename:
            fnamedict = filename.split('?')[1].split('&')
            namelist=[]
            for item in fnamedict:
                namelist.append(item.split("=")[1])

            filename = ("_".join(namelist)) + ".png"
            suffix="png"
        elif suffix not in ['jpg','gif','png']:
            filename = filename + ".png"
            suffix="png"
        filename = filename.replace("%",'').replace("=",'').replace("?",'')
        if img.status_code == 200:
            img.raw.decode_content = True
            with open('static/cache/' + filename,'wb') as imgfile:
                shutil.copyfileobj(img.raw, imgfile)
            if suffix == 'png':
                img = Image.open('static/cache/' + filename)
                width, height = img.size
                wid = (new_h/int(height))*width
                if height > new_h and resize == True:
                    thumb = img.resize((int(wid),new_h))
                    try:
                        thumb.convert('RGB').save('static/cache/'+ filename.split('.')[0] + '.jpg')
                        return "<img src=" + '/static/cache/'+ filename.split('.')[0] + ".jpg height=\"" + str(new_h) + "\" width=\"" + str(wid) + "\">"
                    except Exception as e:
                        print(e)
                        return "<img src=" + '/static/cache/'+ filename + ">"
                else:
                    try:
                        img.convert('RGB').save('static/cache/'+  filename.split('.')[0] + '.jpg')
                        return "<img src=" + '/static/cache/'+ filename.split('.')[0] + '.jpg>'
                    except Exception as e:
                        print(e)
                        return "<img src=" + '/static/cache/'+ filename + ">"
            else:
                img = Image.open('static/cache/'+ filename)
                width, height = img.size
                wid = (new_h/int(height))*width
                if height > new_h and resize == True:
                    try:
                        img.resize((int(wid),new_h))
                        img.save('static/cache/'+ filename.split('.')[0] + "-thumb." + filename.split('.')[-1].lower())
                    except Exception as e:
                        print(e)
                        return "<img src=" + '/static/cache/'+ filename + ">"
                    return "<img src=" + '/static/cache/'+ filename.split('.')[0] + "-thumb." + filename.split('.')[-1].lower() + "  height=\"" + str(new_h) + "\" width=\"" + str(wid) + "\">"
                else:
                    return "<img src=" + '/static/cache/'+ filename + ">"
        else:
            print("Image not retreivable!")
            print(imgUrl)
    except Exception as e:
        print(imgUrl)
        print(e)
        return ''

def parseHTML(html, links=False, resize=True, metaimg=False, domain=None, protocol=None):
    if html == None:
        return ''
    soup = BeautifulSoup(html)
    html_return = []
    try:
        html_return.append("<h1>"+soup.find("title").text+"</h1>")
    except:
        print("HTML has no tilte.")
    tags = ["p","img"]
    if links:
        tags = ["p","img","a"]
    if metaimg:
        tags = ["p", ["meta",{"itemprop": "image"}]]
    for itm in soup.find_all(tags):
        if itm.name == "p":
            html_return.append('<p>' + itm.text + "</p>")
        #elif itm.name == "a":
        elif itm.name == "meta":
            try:
                if itm['itemprop'] == 'image':
                    img_url = checkImageUrl(itm["content"], domain, protocol)
                    html_return.append(saveImageToCache(img_url, resize=resize))
            except Exception as e:
                print(e)
        elif itm.name == "img":
         try:
             img_url = checkImageUrl(itm['src'], domain, protocol)
             html_return.append(saveImageToCache(img_url, resize))
         except Exception as e:
             print(e)
    new_html = "\n".join(list(filter(None, html_return)))
    return new_html


def checkImageUrl(source,domain,protocol):
    if domain != None and protocol != None:
        if source.startswith("http://") or source.startswith("https://"):
            return source
        else:
            if source.startswith("//") :
                return protocol + ":" + source
            elif source.startswith(domain):
                return protocol + "://" + source
            elif source.startswith("/"):
                return protocol + "://" + domain + source
            else:
                return (protocol+'://'+domain+"/"+source)
    else:
        return source