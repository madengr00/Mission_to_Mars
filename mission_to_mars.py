#Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import requests
import pandas as pd

def scrape():
    # ## Step 1 - Scraping from multiple sites
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser =  Browser('chrome', **executable_path, headless=False) 

    #a dictionary to story the scraped data
    mars_data = {}

    ################### NEWS STORY #####################
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #This finds only the top or newest news story
    news_story = soup.find('li', 'slide')

    #This scrapes the tile and teaser paragraph
    for story in news_story:
        news_title = story.find('div','content_title').text
        news_para = story.find('div','article_teaser_body').text
        mars_data["news story"] = (news_title,news_para)
        
        print(news_title)
        print(news_para)


    ################## Featured Image ##################
    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars/'

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #This gets down to background-image:
    background_image = soup.find('article')['style']
    print(background_image)

    #Slice the string and add it to the rest of the path 
    featured_image_url = "https://www.jpl.nasa.gov" + background_image[23:-3]
    print(featured_image_url)
    mars_data["featured_Image"] = (featured_image_url)


    #################### Mars Weather ###################
    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('p','TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    print(mars_weather)
    mars_data["mars_weather"] = (mars_weather)


    ###################### Mars Facts ####################
    # URL of page to be scraped
    url = 'http://space-facts.com/mars/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #read in any tables on the webpage
    Mars_table = pd.read_html(url) 

    #Name the columns
    mars_df = Mars_table[0]
    mars_df.columns = ['descriptor','value']
    #Set descriptor as index
    mars_df.set_index('descriptor',inplace=True)
    mars_df

    #Convert dataframe to HTML table
    mars_html_table = mars_df.to_html()
    mars_html_table
        #Strip unwanted newlines (\n)
    mars_html_table.replace('\n','')
    final_mars_table = mars_df.to_html('mars_table.html')
    mars_data["mars_facts"] = (final_mars_table)


    ################### Mars Hemispheres ##################
    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    products = soup.find('div', class_='collapsible results')
    hemisphere = products.find_all('h3')

    #Create empty lists to store url and title
    image_url_list = []
    title_list =[]

    #Scrape the url and title, store in lists
    for record in hemisphere:
        try:
            #Capture the title
            title_list.append(record)
            #Click on the link
            browser.click_link_by_partial_text('Enhanced')
            #find the Original Image link on the new page
            downloads = browser.find_link_by_text('Sample').first
            link = downloads['href']
            #Capture the sample image url
            image_url_list.append(link)
        except ElementDoesNotExist:
            print("Scraping Complete")

    # use zip() to map values
    titles_and_urls = zip(title_list, image_url_list)
    # convert values to print as a set
    titles_and_urls = set(titles_and_urls)
    print(titles_and_urls)
    mars_data["mars_hemispheres"] = (titles_and_urls)
    
    return(mars_data)

print(scrape())