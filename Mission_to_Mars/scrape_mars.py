from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import requests

import os

ALLOWED_EXTENSIONS = set(['jpg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def scrape_info():


    # def init_browser(): ----------------------------------------------------------
    # Open ChromeDriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
        # browser= init_browser()

    mars_dict={}
    ### NASA Mars News

    #URL for NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # HTML object
    html = browser.html
    
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve all elements that has article information
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    
    ### JPL Mars Space Images - Featured Image

    #URL for JPL Mars Space Images - Featured Image
    space_url = 'https://spaceimages-mars.com/'
    browser.visit(space_url)

    #Use Splinter to navigate the site to find Featured Mars Image
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve all elements that article information
    div = soup.find('div', class_='header')
    a = div.find('a', class_='showimg fancybox-thumbs')
    href = a['href']
    featured_image_url = str(space_url) + str(href)
    

    ### Mars Fact

    #Use pandas to convert the data to a HTML table string
    mars_facts_url = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(mars_facts_url)
    mars_facts_df = tables[0]
    mars_facts_df
    
    mars_facts_df.columns = mars_facts_df.iloc[0]
    cleaned_df = mars_facts_df.drop(mars_facts_df.index[0])
    cleaned_df.set_index('Mars - Earth Comparison', inplace=True)
    cleaned_df
    
    html_table = cleaned_df.to_html()
    html_table.replace('\n', '')
    html_table
    cleaned_df.to_html('table.html')
    
    
    ### Mars Hemispheres

    # Scrape Mars hemisphere title and image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    hem_url = 'https://marshemispheres.com/'
    browser.visit(hem_url)

    #Mars Hemispheres
    html = browser.html
    
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    hemisphere_image_urls = []

    # Retrieve all elements that article information
    section = soup.find('section', id='results-accordian')

    #Retrieve the individual "product" info
    div = section('div', class_='description')

    for product in div:
        #Create dictionary to store title & img url
        dict = {}

        #Gets the title by finding the h3 tag
        title = product.find('h3').text
        dict['title'] = title
    #print(title)

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
        dict['img_url'] = img_url

        hemisphere_image_urls.append(dict)

        #Returns & resets to main URL to get next info
        browser.visit(hem_url)
        html = browser.html
        soup = bs(html, 'html.parser')

    # Create dictionary for all info scraped from sources above
    mars_dict={
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url" : featured_image_url,
        "mars_facts" : cleaned_df,
        "hemisphere_images" : hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()
    return mars_dict

if __name__ == "__main__":
    print(scrape_info())   