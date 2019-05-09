#!/usr/bin/env python
# coding: utf-8

# In[1]:
def scrape():
    scrape_dict = {}

    # Declare Dependencies
    from bs4 import BeautifulSoup
    from splinter import Browser
    import pandas as pd
    import requests
    import requests_html


    # In[2]:


    #Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    from splinter import Browser
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=True)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    news = browser.find_by_css("li.slide div.content_title a").first.text
    news_p = browser.find_by_css("li.slide div.article_teaser_body").first.text
    print(news)
    print(news_p)
    browser.quit()


    # In[3]:


    #JPL Mars Space Images - Featured Image
    #•	Visit the url for JPL Featured Space Image here.
    #•	Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    #•	Make sure to find the image url to the full size .jpg image.
    #•	Make sure to save a complete url string for this image.
    # Example:

    from splinter import Browser
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    #featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    pic = browser.find_by_css("div.carousel_items article.carousel_item").first["style"].lstrip("background-image: url(\"").rstrip("\");")
    pic = "https://www.jpl.nasa.gov/"+pic
    browser.quit()


    # In[4]:


    #https://twitter.com/marswxreport?lang=en
    #scrape the latest Mars weather tweet from the page
    # Example:
    #mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
    res = requests.get('https://twitter.com/marswxreport?lang=en')
    soup = BeautifulSoup(res.content)
    tweet = soup.select_one('.js-tweet-text-container').text



    # In[5]:


    #https://space-facts.com/mars/
    #use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc
    #Use Pandas to convert the data to a HTML table string
    res = requests.get('https://space-facts.com/mars/')
    soup = BeautifulSoup(res.text)
    mytab = pd.read_html(str(soup.find(id='tablepress-mars')))[0]
   # mytab


    # In[6]:


    df = mytab.to_html()


    # In[7]:


    #https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    #Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys `img_url` and `title`.
    #Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    # Example:
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": "..."},
        {"title": "Cerberus Hemisphere", "img_url": "..."},
        {"title": "Schiaparelli Hemisphere", "img_url": "..."},
        {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    ]


    # In[21]:


    res = requests.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    soup = BeautifulSoup(res.content)

    items = soup.select('.item a')
    hemisphere_image_urls = []
    #print(len(items))
    for item in items:
        pageurl = 'https://astrogeology.usgs.gov'+item.get("href")
        #pageurl = 'https://astrogeology.usgs.gov'+title.find('a').get('href')
        title = item.find('h3').text
        res = requests.get(pageurl)
        url = BeautifulSoup(res.text).find(class_='downloads').find_all('a')[0].get('href')
        hemisphere_image_urls.append({'title': title, 'img_url': url})


    # In[ ]:
    scrape_dict.update({'twitter':tweet,'featured_img_url':pic, 'dfhtml':df, 'newsfeed':news, 'newsparagraph':news_p, "hemisphere_image_urls":hemisphere_image_urls})
    return scrape_dict


from flask import Flask, render_template
import pymongo

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
@app.route("/")
def echo():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client["mars"]
    mycol = db["mars"]
    data = mycol.find_one()
    return render_template("index.html",data=data)


# Bonus add a new route
@app.route("/scrape")
def scrape_data():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client["mars"]
    #db["mars"]
    # If collection music exists, drop it so the new top 10 information will replace it
    db.mars.drop()


    # #Create new empty music-albums collection
    db.create_collection("mars")
    mycol = db["mars"]
    mycol.insert_one(scrape())
    return ("", 204)