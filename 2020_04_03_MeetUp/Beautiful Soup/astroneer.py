"""
What's really funny is that I edited the astroneer wiki to: add information, make it easier to scrape, and be more consistent between pages and the admin is so possessive that he undid all my edits and banned me for 3 days. As a result, this script doesn't accurately scrape data from the astroneer wiki.
"""
import os
import sys
import requests
import bs4
import re
from pprint import pprint as pp


def get_recipe_table(url):
    page_req = requests.get(url)  # get the page
    page_req.raise_for_status()  # check for errors
    soup = bs4.BeautifulSoup(page_req.text, 'lxml')  # soupify!

    # select tables that are direct children of a div tag, with a class attr containing "zebra" but not "recipeTable"
    table = soup.select('div > table[class~=zebra]:not(table[class~=recipeTable])')
    return table[0]  # since we should only get one table


def process_recipe_row(tr):
    url_master = 'https://astroneer.gamepedia.com'  # this is used to follow links to individual item pages and extract the infobox
    try:
        outp, inp = tr.find_all('td')  # get the two cells and assign them to the output and input variables
        olink = outp.find('a', title=True)  # find the first anchor tag with a title
        print(olink.get('title'))
        out_str = olink.get('title')  # there should only be two links in the outp cell, and both "title" attributes are the same

        # go to the item's page and pull the infobox data
        item_url = url_master + olink.get('href')
        info = process_info_box(item_url)
        
        strs = list()
        for i in inp.strings:  # grab all the text that is displayed on screen and not any tag info
            strs.append(i)  # put those strings in a list
        print(strs)
        # do some ETL on the recipe list, then output the recipe with some other info
        return out_str, {'recipe': process_ing_list(strs), 'size': info['size'], 'research_cost': info['research_cost']}
    except ValueError as e:  # any error in the above "try" block means we're in a header row, not a row with any data
        print(f'{e}, skipping header row...')
        return None, None


def process_info_box(url):
    item_page = requests.get(url)  # get the page
    item_page.raise_for_status()  # check for errors
    soup = bs4.BeautifulSoup(item_page.text, 'lxml')  # soupify!
    
    info_box = soup.find('table', class_='infoboxtable')  # there should be only one table with a "class" attr that is exactly 'infoboxtable'
    # info_box = soup.find('table', attrs={'class': 'infoboxtable'})  # alternate way of finding the same table
    rows = info_box.find_all('tr')  # grab all the rows out of the table
    row_strings = list()
    info = dict()
    # remap_dict is for internal use only
    remap_dict = {'Tier': 'size',
                  'Group': 'group',
                  'Type': 'type',
                  'Crafted at': 'crafted_at',
                  'Recipe': 'recipe',
                  'Unlock Cost': 'research_cost'}
    for i in rows:  # strip line breaks and commas out (as this will ultimately be a csv)
        row_strings.append([j.replace('\n', '').replace(',', '') for j in i.strings])
    row_strings = row_strings[-6:]  # this is some evil magic number bs; it works but it's fragile
    
    for i in row_strings:  # this for loop iterates through each row of the table and extracts data under the assumption that "key" appears before "value" _somewhere_
        attr = ''
        while(len(i)):  # because we're popping list items, the len(list) will be 0 when finished with that row
            term = i.pop(0)
            # print(f'term: {term}')
            if term in remap_dict.keys():  # is this data that we're looking for?
               attr = term
            elif len(term) > 3 and term != 'Bytes':  # special case for the research_cost 
                try:
                    info[remap_dict[attr]] = term
                except KeyError:
                    print(f'Infobox error: attr={attr}, term={term}')
            
            # print(info)
    info['research_cost'] = info.get('research_cost', 'Unlocked').strip()  # data validation for the cost and some formatting
    return info


def process_ing_list(ing_list):
    ing_dict = dict()
    count_re = re.compile(' ?x(\d)\n?')  # regex with a group for the count
    ing_list.pop(0)  # remove the leading whitespace
    last_ing = ''  # so we can remember the last ingredient name while checking for a quantity string
    while(len(ing_list)):
        term = ing_list.pop(0)  # reading the list left to right
        count = count_re.search(term)  # test if the current term is a quantity string
        if len(term) > 3 and count is None:  # if no amount is specified, count is 1
            ing_dict[term] = 1
            last_ing = term
        elif count is not None:  # if an amount is specified, set the count
            ing_dict[last_ing] = int(count.group(1))
    
    return ing_dict


def process_recipe_table(table):
    results = dict()
    rows = table.find_all('tr')  # pull all the rows out of a table
    for i in rows:
        name, data = process_recipe_row(i)
        if name != None:  # if we successfully interpreted a recipe row, add the data to the results dict
            results[name] = data
    return results


def expand_recipe(recipe):
    r = list()
    for k, v in recipe.items():  # k = ingredient, v = count
        for i in range(v):
            r.append(k)  # adds each ingredient to the list a number of times equal to its count
    while len(r) < 4:  # add empty strings to bring the ingredient count up to four, to make formatting the csv easier
        r.append('')
    return r


def get_power_data():
    url = 'https://astroneer.gamepedia.com/Power'
    power_req = requests.get(url)
    power_req.raise_for_status()
    soup = bs4.BeautifulSoup(power_req.text, 'lxml')
    flow_rate = 'Flow Rate\n'
    capacity = 'Capacity\n'
    consumption = 'Consumption Rate\n'
    prefix = ';'
    results = dict()
    tables = soup.find_all('table', limit=3)
    for table in tables:
        # print(table.attrs)
        rows = table.find_all('tr')#, limit=5)
        header = rows[0]
        print(head_strs := [j for j in header.strings])
        # for i in rows:
        #     print([j for j in i.strings])
        if flow_rate in head_strs:
            # do producers
            print('producers')
            prefix = '+'
        elif consumption in head_strs:
            # do consumers
            print('consumers')
            prefix = '-'
        elif capacity in head_strs:
            # do batteries
            print('batteries')
            prefix = ''

        for i in rows[1:]:
                strs = [j.replace('\n', '') for j in i.strings]
                results[strs[1]] = prefix + strs[4]
    return results


# these are the pages we're going to be scraping
urls = ['https://astroneer.gamepedia.com/Large_Printer',
        'https://astroneer.gamepedia.com/Small_Printer',
        'https://astroneer.gamepedia.com/Medium_Printer',
        'https://astroneer.gamepedia.com/Chemistry_Lab',
        'https://astroneer.gamepedia.com/Smelting_Furnace',
        'https://astroneer.gamepedia.com/Backpack',
        ]
tables = dict()
crafting = dict()

for i in urls:
    tables[os.path.basename(i)] = get_recipe_table(i)  # basename(i) returns everything after the last '/'

for k, v in tables.items():  # k = name of crafting station, v = recipe table for that station
    crafting[k] = process_recipe_table(v)

power_data = get_power_data()
# write the csv
csv = list()
for k in crafting.keys():  # k = crafting station
    for v in crafting[k].keys():  # v = item name
        r = expand_recipe(crafting[k][v]['recipe'])  # recipe for item v
        csv.append(f'{r[0]},{r[1]},{r[2]},{r[3]},{v},{k},{crafting[k][v]["research_cost"]},{power_data.get(v, "")},{crafting[k][v]["size"]}')  # look at that beautiful f-string

pp(crafting)
# output to disk
with open('recipes.csv', mode='w') as r:
    r.write('\n'.join(csv))