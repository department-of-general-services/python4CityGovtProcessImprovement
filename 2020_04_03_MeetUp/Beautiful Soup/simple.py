"""
Simple examples of using Beautiful Soup 4 for the PCGI meetup

requires:
    bs4
    requests
"""

import bs4
from bs4 import UnicodeDammit
import requests
import os
import sys
import re
from pprint import pprint as pp

url = 'https://www.xkcd.com/2286/'  # define the url we're scraping the page of
url_req = requests.get(url)  # get the page
url_req.raise_for_status()  # check for errors
page_text = url_req.text  # assign the page text to a variable
soup = bs4.BeautifulSoup(page_text, 'lxml')  # soupify!

links = soup.find_all('a')  # find all the 'a' tags (i.e., '<a ...')
# links = soup.find_all('a', rel=True)  # find all the 'a' tags that also have a 'rel' attribute
# links = soup.find_all('a', attrs={'href': re.compile('https:')})  # find all 'a' tags that have 'https:' _somewhere_ in the 'href' attribute
# links = soup.find_all('a', href=re.compile('https:'))  # different way to find all 'a' tags that have 'https:' _somewhere_ in the 'href' attribute
for link in links:
    # if 'xkcd' not in link.get('href'):
    print(link)  # print the 'a' tags
    # print(link.get('href'))  # just print the 'href' attribute

# images = soup.find_all('img')  # finding all the image tags
# # images = soup.find_all('img', attrs={'alt': True})  # finding all the image tags that have an "alt" attribute, regardless of what the value is
# # images = soup.find_all('img', alt=True)  # alternate way of finding all the image tags that have an "alt" attribute, regardless of what the value is
# for image in images:
#     print(image)
#     # print(image.get('alt'))

# class_tags = soup.find_all(True, attrs={'class': True})  # find all tags that have a "class" attribute
# # class_tags = soup.find_all(True, class_=True)  # another way of doing the same. Note the underscore after "class" in this instance. That's necessary because "class" is a reserved word in python
# # class_tags = soup.find_all(True, class_=True, id=False)  # adding a second criteria; the tag must have a "class" attribute but must NOT have an "id" attribute
# for tag in class_tags:
#     print(tag.name, tag.attrs)

# imgs_and_links = soup.find_all(['img', 'a'])
# # imgs_and_links = soup.find_all(['img', 'a'], limit=10)
# for tag in imgs_and_links:
#     print(tag.name, tag.attrs)
    
    
# using a custom filter to be more selective 
# def custom_criteria(tag):
#     if tag.has_attr('href'):
#         return 'https:' in tag.get('href') and 'xkcd' not in tag.get('href')  # selecting for links that don't go to somewhere in xkcd.com
#     else:
#         return False


# outside_links = soup.find_all(custom_criteria)
# for link in outside_links:
#     print(f'{link.name}, {link.get("href")}')