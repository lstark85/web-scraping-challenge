#!/usr/bin/env python
# coding: utf-8

# # <font color='blue'> Step 1 - Scraping </font>

# In[1]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


# import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


# In[3]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


#Dictionary
# Create dictionary for all info scraped from sources above
mars_data={
    "news_title" : [],
    "news_p" : [],
    "featured_image_url" : [],
    "mars_facts" : [],
    "img_url" : [],
    "title" : []
}


# ## Nasa Mars News

# In[5]:


#URL for NASA Mars News
url = 'https://redplanetscience.com/'
browser.visit(url)


# In[6]:


# HTML object
html = browser.html
    
# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')

# Retrieve all elements that has article information
news_title = soup.find('div', class_='content_title')
news_p = soup.find('div', class_='article_teaser_body')

print(news_title.text)
print(news_p.text)
mars_data["news_title"].append(news_title)
mars_data["news_p"].append(news_p)


# ## JPL Mars Space Images - Featured Image

# In[7]:


#URL for JPL Mars Space Images - Featured Image
space_url = 'https://spaceimages-mars.com/'
browser.visit(space_url)


# In[8]:


#Use Splinter to navigate the site to find Featured Mars Image
html = browser.html

# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')

# Retrieve all elements that article information
div = soup.find('div', class_='header')
a = div.find('a', class_='showimg fancybox-thumbs')
href = a['href']
featured_image_url = str(space_url) + str(href)
print(featured_image_url)
mars_data["featured_image_url"].append(featured_image_url)


# In[9]:


browser.quit()


# ## Mars Facts

# In[10]:


#Use pandas to convert the data to a HTML table string
mars_facts_url = 'https://galaxyfacts-mars.com'
tables = pd.read_html(mars_facts_url)
mars_facts_df = tables[0]
mars_facts_df


# In[11]:


mars_facts_df.columns = mars_facts_df.iloc[0]
cleaned_df = mars_facts_df.drop(mars_facts_df.index[0])
cleaned_df.set_index('Mars - Earth Comparison', inplace=True)
cleaned_df


# In[12]:


#Convert data to HTML table string
html_table = cleaned_df.to_html()
html_table.replace('\n', '')
html_table


# In[13]:


cleaned_df.to_html('table.html')


# ## Mars Hemispheres

# In[14]:


#Mars Hemispheres
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

hem_url = 'https://marshemispheres.com/'
browser.visit(hem_url)


# In[15]:


#Mars Hemispheres
html = browser.html
    
# Parse HTML with Beautiful Soup
soup = bs(html, 'html.parser')

hemisphere_image_urls = []

# Retrieve all elements that article information
section = soup.find('section', id='results-accordian')

#Retrieve the individual "product" info
div = section.find_all('div', class_='description')

for product in div:
    #Create dictionary to store title & img url
    dict = {}

    #Gets the title by finding the h3 tag
    title = product.find('h3').text
    
    print(title)

    #Clicks the link with that title
    browser.links.find_by_partial_text(title).click()

    #Sets the html to the new page's html
    html = browser.html
    soup = bs(html, 'html.parser')

    #Clicks the "Open" to get the full image
    browser.links.find_by_partial_text('Open').click()
    img = soup.find('img', class_='wide-image')['src']
    #Adds the the first part of the img url
    img_url = str(hem_url + img)
    print(img_url)

    mars_data['title'].append(title)
    mars_data['img_url'].append(img_url)
    hemisphere_image_urls.append(dict)

    #Returns & resets to main URL to get next info
    browser.visit(hem_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
browser.quit()


# In[16]:


mars_data


# In[17]:


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[18]:


db = client.marsdata_db
marsdata = db.marsdata
marsdata.insert_one(mars_data)


