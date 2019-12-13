import requests
import urllib.request
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from urllib.request import urlopen
from . import models

BASE_CRAIGSLIST_URL = 'http://www.amazon.com/s?k={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, "base.html")


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response_ooo = urlopen(final_url).read()
    data = response_ooo
    soup = BeautifulSoup(data, features='html.parser')

    
    post_listings = soup.find_all('div', {'class': 's-include-content-margin s-border-bottom'})
   
    final_postings = []


  

    for post in post_listings:
        post_title = post.find(class_='a-size-medium a-color-base a-text-normal').text
        scrape_url = post.find(class_='a-link-normal a-text-normal').get('href')
        post_url = 'https://www.amazon.com' + scrape_url

        if post.find(class_='s-image').get('src'):
            post_img = post.find(class_='s-image').get('src')
        else:
            post_img = ''

        if post.find(class_='a-offscreen'):
            post_price = post.find(class_='a-offscreen').text
        else:
            post_price = 'I padisponueshem per mometin.'


        final_postings.append((post_title, post_url, post_price, post_img))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'myapp/index.html', stuff_for_frontend)
