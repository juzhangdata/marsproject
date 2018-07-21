
# coding: utf-8

# In[1]:


def scrape():
    # Dependencies
    import pandas as pd
    from bs4 import BeautifulSoup as bs
    import requests
    from splinter import Browser

    # -----------------------------------------------------------------------------------------------------
    # NASA Mars News
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    # Get response from url with requests
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(news_url)

    # Use beautiful soup to parse response
    soup = bs(response.text, "html.parser")
    soup.prettify()

    # Get title and text of latest news
    # Assign the text to variables
    news_title = soup.find("div", class_="content_title").text.strip()
    news_p = soup.find("div", class_="rollover_description_inner").text.strip()

    # -----------------------------------------------------------------------------------------------------
    # JPL Mars Space Images - Featured Image
    # Get response from url with requests
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    response = requests.get(image_url)

    # Set up controller of chrome
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    browser.visit(image_url)
    browser.click_link_by_partial_text("FULL IMAGE")
    html = browser.html
    soup = bs(html, "html.parser")
    result = soup.find("a", class_="button fancybox")
    link = result["data-fancybox-href"]

    # Save a complete url string for this image
    featured_image_url = "https://www.jpl.nasa.gov" + link

    # -----------------------------------------------------------------------------------------------------
    # Mars Weather
    # Get  the latest Mars weather tweet from twitter
    url = "https://twitter.com/marswxreport?lang=en"
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    # Save the tweet text for the weather report as a variable
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()

    # -----------------------------------------------------------------------------------------------------
    # Mars Facts
    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[0]
    df = df.set_index(0)
    df["Description"] = "Value"

    # Use Pandas to convert the data to a HTML table string
    df.to_html("mars_facts.html", header=False)

    # -----------------------------------------------------------------------------------------------------
    # Mars Hemispheres 
    home_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response = requests.get(home_url)

    # Use beautiful soup to parse response
    soup = bs(response.text, "html.parser")
    hemisphere_image_urls = []

    # Get titles
    titles = []
    results = soup.find_all("h3")
    for result in results:
        title = result.text.strip()
        titles.append(title)

    # get urls
    click_urls=[]
    results = soup.find_all("a", class_="itemLink product-item")
    for result in results:
        click_url = "https://astrogeology.usgs.gov"+result["href"]
        click_urls.append(click_url)
    # print(click_urls)

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    full_image_urls = []
    for url in click_urls:
        browser.visit(url)
        html = browser.html
        soup = bs(html, "html.parser")
        url = soup.find("img", class_="wide-image")["src"]
        full_image_url = "https://astrogeology.usgs.gov" + url
        full_image_urls.append(full_image_url)
    print(full_image_urls)

    # make a dictionary for all the full urls
    for i in range(len(titles)):
        hemisphere_image_urls.append(
        {
            "title": titles[i],
            "img_url": full_image_urls[i]
        })
    print(hemisphere_image_urls)
    
    data_results = {
        "news_title": news_title,
        "news_p" : news_p,
        "featured_image_url": featured_image_url,
        "mars_weather" : mars_weather,
        "hemisphere_image_urls" : hemisphere_image_urls
    }
    
    return data_results

