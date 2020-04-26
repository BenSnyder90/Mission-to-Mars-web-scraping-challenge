# web-scraping-challenge
CWRU Data Analytics Bootcamp - HW 12
--------------------
## Objectives
* Use Splinter and Beautiful Soup to parse various websites HTML code
* Store text, tables, and image sources using parsed data using MongoDB
* Display stored info on a website in a single HTML page

---------------------
## Contents
<b><h2>/Mission_To_Mars/</b></h2>
* <b>mission_to_mars.ipynb</b> - Jupyter Notebook that performs the initial scraping of each site. Markdown includes steps taken to find the desired information via HTML code
* <b>scrape_mars.py</b> - Python script that uses the parsing methods from the Jupyter Notebook that returns a dictionary object to be inserted into MongoDB
* <b>app.py</b> - Python Flask app that loads the Index.html as a template and runs the scrape_mars.py parsing script, and loads the parsed info through MongoDB to be used by the template
* <b>chromedriver.exe</b> - Browser used by Splinter to parse HTML
<b><h2>/templates/</b></h2>
* <b>Index.html</b> - HTML page that displays the information parsed through various Mars websites and creates a dashboard of information. Styled using Bootstrapping
