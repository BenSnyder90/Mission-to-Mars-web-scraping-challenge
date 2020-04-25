# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.

#Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function 
#called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.

#Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.

#Store the return value in Mongo as a Python dictionary.

#Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.

#Create a template HTML file called index.html that will take the mars data dictionary 
#and display all of the data in the appropriate HTML elements.

#Dependencies

from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = init_browser()
    mars_data = {}
    #Scrape the NASA Mars News Site (https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

    #Parse the html of the site
    #LOOK AT HTML TO FIND THE RIGHT TAGS
    #find() function to store News Title and Paragraph Text <p?> in variables

    #Title <div class="content_title">
    #Paragraph Text <div class = "article_teaser_body">

    url = "https://mars.nasa.gov/news"
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_title = soup.find_all('div', class_='content_title')[1].text
    mars_paragraph = soup.find_all('div', class_="article_teaser_body")[0].text


    #Visit the url for JPL Featured Space Image here (https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    #Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    #Make sure to find the image url to the full size .jpg image.
    #Make sure to save a complete url string for this image.

    #Use splinter to browse(url)
    #LOOK AT SITE TO GET TO THE CURRENT FEATURED MARS IMAGE TAGS
    #Use splinter to click on full size image
    #Parse HTML to get full URL and store in variable

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    browser.click_link_by_partial_text('FULL')
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    featured_url = soup.find('img', class_='fancybox-image')['src']
    featured_image_url = 'https://www.jpl.nasa.gov'+featured_url



    #Visit the Mars Weather twitter account here (https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather

    #LOOK AT HTML OF SITE when not logged into Twitter
    #Parse HTML of the URL and use the find() funtion to get the tag of the latest tweet
    #Save it as a variable


    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    time.sleep(3)

    html = browser.html
    soup = bs(html, 'html.parser')


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

    mars_df.columns = ['Description','Value']

    mars_df = mars_df.set_index('Description')

    mars_table = mars_df.to_html(classes = 'table table-striped')


    # Mars Hemispheres
    #Visit the USGS Astrogeology site here (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.
    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    #Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    #Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    #Use splinter to browse(url)
    #Parse HTML to get the destinations to click the image links
    #LOOK AT HTML FOR THE TAGS
    #Make an empty list
    #Use for loop to run through the images
    #Click on the images to get the image URL
    #Parse HTML to get image title
    #Make dictionary of title and image URL
    #Append dictionary to list
    #End For


    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    mars_hemi = []
    html = browser.html
    soup = bs(html,'html.parser')

    hemi_links = soup.find_all('div', class_='item')

    for x in hemi_links:
        image_title = x.find('h3').text
        image_title = image_title.replace('Enhanced','')
        image_title = image_title.rstrip(' ')

        image_url = x.find('a')['href']
        img_url = "https://astrogeology.usgs.gov"+ image_url

        browser.visit(img_url)
        html = browser.html
        soup = bs(html,'html.parser')
        hemi_img = soup.find('img', class_="wide-image")['src']
            
        hemi_data = {
            'img_url' : 'https://astrogeology.usgs.gov'+hemi_img,
            'title': image_title
        }
    
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

    browser.quit()

    return mars_data

if __name__ == '__main__':
    scrape()