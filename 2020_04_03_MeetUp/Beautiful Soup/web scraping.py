"""
python 3
web scraping practice using:
    requests
    beautiful soup 4

a[::-1] == reversed list  ([start:end:step])

goal: download all xkcd comics, number and title them appropriately
"""

import requests
import bs4
import os
# import time

# this block of code sets up the folder where we place the images and sets the url we start working with
# os.chdir('/comics/')
url_master = 'http://xkcd.com'
url = 'http://xkcd.com'
comic = 'xkcd'
folder = comic
# folder = ' '.join([comic, time.strftime('%Y-%m-%b')])
os.makedirs(folder, exist_ok=True)
os.chdir('./' + folder)


while not url.endswith('#'):  # ending with an octothorpe ('#') indicates we've hit the very first page
    print('downloading', url)
    # get the page and parse the html using the lxml library
    comic_page = requests.get(url)  # make the http request
    comic_page.raise_for_status()  # check the reponse, raises an exception if something went wrong
    soup = bs4.BeautifulSoup(comic_page.text, 'lxml')  # soupify!

    prev_data = soup.select('a[rel="prev"]')[0]  # get the anchor tag that links to the previous page
    prev_link = prev_data.get('href')  # get the actual link (sorta)
    if not url.endswith('.com'):
        num = os.path.split(url[:-1])[1]  # get the number of the comic from the url by splitting the url after deleting the trailing '/'
    else:
        try:
            num = int(prev_link[1:-1]) + 1  # strip the leading and trailing '/', cast to int, add 1 because this should only run when on the front page
            num = str(num)  # no matter what, cast num to a string
        except:
            # print error number instead
            num = 'XXXX'
            print("no number detected")
    # print(num)
    comic_data = soup.select('#comic img')  # select the img tag that is a direct child of a tag with id=comic
    if comic_data != []:  # check that we actually got something
        comic_url = comic_data[0].get('src')  # get the source of the image
        try:
            comic_req = requests.get('https:' + comic_url)  # add the https to the source we just got
            comic_req.raise_for_status()  # check that for errors

            # the comic is already named as the title, now we just stick a 4-digit number at the beginning to make sorting by alpha and sorting by time the same result
            with open(num.zfill(4) + ' ' + os.path.basename(comic_url), 'wb') as c:
                for chunk in comic_req.iter_content(100000):
                    c.write(chunk)
        except Exception as e:
            print(e)

    url = url_master + prev_link  # build the link to the previous page and follow it