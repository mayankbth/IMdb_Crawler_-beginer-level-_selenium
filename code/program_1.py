from selenium import webdriver

# import this for select tag
from selenium.webdriver.support.ui import Select

from selenium.webdriver.common.by import By

import pandas as pd
import time

from bs4 import BeautifulSoup

import requests


driver = webdriver.Chrome('E:\Crawling\IMdb Crawler\chromedriver_win32\chromedriver.exe')
driver.get("https://www.imdb.com/")

# to maximize the window after open
driver.maximize_window()

# After clicking on the dropdown we want to wait 
# for the one second (wating for the elements to be loaded)
time.sleep(1)

# class name locator
dropdown = driver.find_element(By.CLASS_NAME, "ipc-icon--arrow-drop-down")
dropdown.click()

time.sleep(1)

# advanced search form dropdown menue
# with link text the spelling should be identical as on website
# click on "Advanced Search"
element = driver.find_element_by_link_text('Advanced Search')
element.click()

time.sleep(1)

# click on "Advanced Title Search"
element = driver.find_element_by_link_text('Advanced Title Search')
element.click()

time.sleep(1)

# select "Feature Film"
feature_film = driver.find_element_by_id('title_type-1')
feature_film.click()

# select "TV Movie"
tv_movie = driver.find_element_by_id('title_type-2')
tv_movie.click()

# min date
min_date = driver.find_element_by_name('release_date-min')
min_date.click()
# to type something we need to use the keys function
min_date.send_keys('1990')

# max date
max_date = driver.find_element_by_name('release_date-max')
max_date.click()
max_date.send_keys('2020')

# rating min
rating_min = driver.find_element_by_name('user_rating-min')
rating_min.click()
dropdown_2 = Select(rating_min)
dropdown_2.select_by_visible_text('1.0')

# rating max
rating_max = driver.find_element_by_name('user_rating-max')
rating_max.click()
dropdown_3 = Select(rating_max)
dropdown_3.select_by_visible_text('10')

# oscar nominated
oscar_nomited = driver.find_element_by_id('groups-7')
oscar_nomited.click()

# colour film
color = driver.find_element_by_id('colors-1')
color.click()

# language
language = driver.find_element_by_name('languages')
dropdown_4 = Select(language)
dropdown_4.select_by_visible_text('English')

# 250 results
result_count = driver.find_element_by_id('search-count')
dropdown_5 = Select(result_count)
dropdown_5.select_by_index(2)

# submit
submit = driver.find_element_by_xpath('(//button[@type="submit"])[2]')
submit.click()

time.sleep(1)

# current
current_url = driver.current_url

# get request
response = requests.get(current_url)
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print(response.status_code)
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# soup object
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)

# result itmes (starting point)
# list_items = soup.find_all('div', {'class': 'lister-item mode-advanced'})
list_items = soup.find_all('div', {'class': 'lister-item'})
# print(len(list_items))
# the length of "list_items" should be 250

"""
    data we want to extract
        1. movie title
        2. year
        3. duration
        4. genere
        5. rating
"""

# # movie title
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print(list_items[0].find('h3').find('a').get_text().strip())
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# # year
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print(list_items[0].find('h3').find('span', {'class': 'lister-item-year text-muted unbold'}).get_text().replace('(','').replace(')','').strip())
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# # duration
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print(list_items[0].find('span', {'class': 'runtime'}).get_text().strip())
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# # genere
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print(list_items[0].find('span', {'class': 'genre'}).get_text().strip())
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# # rating
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print(list_items[0].find('div', {'class': 'inline-block ratings-imdb-rating'}).get_text().strip())
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# lsit comprehension
movie_title = [result.find('h3').find('a').get_text().strip() for result in list_items]
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print(movie_title)
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

year = [result.find('h3').find('span', {'class': 'lister-item-year text-muted unbold'}).get_text().replace('(','').replace(')','').strip() for result in list_items]
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print(year)
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

duration = [result.find('span', {'class': 'runtime'}).get_text().strip() for result in list_items]
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print(duration)
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# genere = [result.find('h3').find('span', {'class': 'genre'}).get_text().strip() for result in list_items]
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print('genere')
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

rating = [result.find('div', {'class': 'inline-block ratings-imdb-rating'}).get_text().strip() for result in list_items]
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print(rating)
# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# print('movie_title')
# print('year')
# print('duration')
# print('genere')
# print('rating')

imdb_df = pd.DataFrame({'Movie Title': movie_title, 'Year': year, 'Duration': duration, 'Rating': rating})

# print(imdb_df)

# output in excel
imdb_df.to_excel('imdb_multiple_pages.xlsx', index=False)