# -*- coding: utf-8 -*-

import pymongo
import time
from bs4 import BeautifulSoup
from urllib2 import urlopen
from PIL import Image

client = pymongo.MongoClient("localhost", 27017)
db = client.parser

url = "http://nnov.am.ru/all/search/"
url_page = "http://nnov.am.ru/all/search/?p="


def get_count_pages(url):
    pages = db.pages.find_one()
    if pages is None:
        html_doc = urlopen(url).read()
        soup = BeautifulSoup(html_doc)

        count_pages = soup.find("div", class_="paginator-amount").get_text()
        count = count_pages.split()
        pages = count[3]

        db.pages.remove()
        db.pages.save({"count": pages})

        return pages
    else:
        return pages["count"]


def parse_page(url_page):
    html_doc = urlopen(url_page).read()
    soup = BeautifulSoup(html_doc)

    adverts = soup.find_all("div", class_="title")
    for advert in adverts:
        advert_url = advert.a.get("href")
        print advert.a.get("href")
        db.am_ru.insert({"advert_url": advert_url})


def parse_pages(count_pages):
    for i in xrange(0, int(count_pages)):
        print i
        page = url_page + str(i)
        print page
        parse_page(page)


def parse_advert(url_advert):
    for advert in adverts:
        print advert["advert_url"]

# db.pages.remove()
# db.am_ru.remove()
# pages = get_count_pages(url)
# print pages
# parse_pages(pages)

# for advert in db.am_ru.find():
#     print advert.get("advert_url")
#     advert_url = str(advert.get("advert_url"))
#     print advert_url
#     html_doc = urlopen(advert_url).read()
#     soup = BeautifulSoup(html_doc)
#
#     images = soup.find("li", class_="b-rama-thumbs__item")
#     for image in images:
#         image_soup = BeautifulSoup(image)
#         src = image_soup.li
#         print src
#     #print type(images)
#     #db.am_ru_adverts.insert({"advert_html": advert_html})
#
#     time.sleep(300)

html_doc = urlopen("http://nnov.am.ru/used/hyundai/ix35/avs-avtoregion-nn--9fa3edb9/#snp3").read()
soup = BeautifulSoup(html_doc)

images = []
ul = soup.find_all("li", class_="b-rama-thumbs__item")
for li in ul:
    images.append(li.a["data-original"])

ii = 0
for image in images:
    fileimage = urlopen(image).read()
    f = open(str(ii)+".jpg", "wb")
    f.write(fileimage)
    f.close
    print image
    img = Image.open(str(ii)+".jpg")
    width, height = img.size
    left = 0
    top = 0
    right = width
    bottom = height - 100
    img2 = img.crop([left, top, right, bottom])
    img2.load()
    img2.save(str(ii)+"-crop.jpg")
    ii += 1