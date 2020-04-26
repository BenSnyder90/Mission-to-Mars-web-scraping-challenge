#Dependencies

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time

def init_browser():
    #Use chromedriver.exe as the Browser used for Splinter
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    #Load browser
    browser = init_browser()

    #Create empty dictionary of data to be stored after parsing data
    mars_data = {}

    #Scrape the NASA Mars News Site (https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text.
  
    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    #Let the site load
    time.sleep(3)

    #Parse the html of the site
    html = browser.html
    soup = bs(html, 'html.parser')

    #Store first title and paragraph text using the find_all function and finding the right index value
    mars_title = soup.find_all('div', class_='content_title')[1].text
    mars_paragraph = soup.find_all('div', class_="article_teaser_body")[0].text


    #Visit the url for JPL Featured Space Image here (https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    
    #Use splinter to browse(url)
    #LOOK AT SITE TO GET TO THE CURRENT FEATURED MARS IMAGE TAGS
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    #Use splinter to click on full size image by using the partial text click function
    browser.click_link_by_partial_text('FULL')
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')
    #Parse HTML to get full URL and store in variable
    featured_url = soup.find('img', class_='fancybox-image')['src']
    featured_image_url = 'https://www.jpl.nasa.gov'+featured_url



    #Visit the Mars Weather twitter account here (https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather

    #LOOK AT HTML OF SITE when not logged into Twitter
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    #Wait for the site to load before parsing the page
    time.sleep(3)

    #Parse the page using Splinter
    html = browser.html
    soup = bs(html, 'html.parser')

    #Twitter uses this class for every line of text. The 28th position in this list contains the latest tweet.
    #Store that text in a variable
    mars_weather = soup.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")[27].text



    #Visit the Mars Facts webpage here (https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    #Use Pandas to convert the data to a HTML table string.

    #Use pandas to read_html() of the URL
    #Look at created dataframe to get the planet facts table from the index values
    #Make a dataframe of just the planet facts index 
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    tables = pd.read_html(url)

    #First table appears to be info for Mars
    mars_df = tables[0]
    #Change column names
    mars_df.columns = ['Description','Value']
    #Set index to the Description col
    mars_df = mars_df.set_index('Description')
    #Use pandas .to_html() function to save it as a striped-table HTML code
    mars_table = mars_df.to_html(classes = 'table table-striped')


    # Mars Hemispheres
    
    #Use Splinter to browse the Hemispheres site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    #Make an empty list to store hemisphere data
    mars_hemi = []

    #Parse the HTML
    html = browser.html
    soup = bs(html,'html.parser')

    #Get list of hemispheres using HTML parsing with class "item"
    hemi_links = soup.find_all('div', class_='item')

    #Make a for loop to run through the list of the hemisphere items
    for x in hemi_links:

        #Get the title text from the parser find() function and clean up the text showing only the Hemisphere titles
        image_title = x.find('h3').text
        image_title = image_title.replace('Enhanced','')
        image_title = image_title.rstrip(' ')

        #Get the image URL using find() function
        image_url = x.find('a')['href']
        #Store the image URL for the browser
        img_url = "https://astrogeology.usgs.gov"+ image_url
        #Visit the image page to get the full size image URL

        browser.visit(img_url)
        #Parse the page and get the full size image URL
        html = browser.html
        soup = bs(html,'html.parser')
        #Store the URL in a variable
        hemi_img = soup.find('img', class_="wide-image")['src']
        
        #Store each hemisphere data in dict
        hemi_data = {
            'img_url' : 'https://astrogeology.usgs.gov'+hemi_img,
            'title': image_title
        }
        #Add each dict to the hemisphere list
        mars_hemi.append(hemi_data)

    #Store all of the scraped data into a Python dictionary
    mars_data = {
        'mars_title':mars_title,
        'mars_paragraph':mars_paragraph,
        'featured_img_url':featured_image_url,
        'mars_weather':mars_weather,
        'mars_table': mars_table,
        'mars_hemi': mars_hemi
    }
    #Close browser
    browser.quit()

    #Returns the data dictionary
    return mars_data

if __name__ == '__main__':
    scrape()