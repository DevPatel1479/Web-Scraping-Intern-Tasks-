# Adding the dependencies for the project

import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


# Method which will return the product name using the soup object if found

def getProductDetails(soup):
    try:
        product_title = soup.find('span', attrs = {'id':'productTitle'})   # It checks for the product name
                                                                            # using the find() and
                                                                           # find the span element content
                                                                           # hidden in span tag with
                                                                           # id productTitle
                                                                           # associated with the soap object
        product_name = product_title.text.strip()
    except:
        return ""
    return product_name                                # This statement will return the product name if found on
                                                        # the web page of amazon


# # Method which will return the product price using the soup object if found
def getProductPrice(soup):
    try:
        product_price = soup.find('span', attrs = {'class' : 'a-price-whole'})   # This Statement will find the product price
                                                                                # using soup.find() for that span
                                                                                # element whose class name is 'a-price-whole'
        product_pr = product_price.text.strip()
    except:
        return ""
    return product_pr


# Method which will return the product ratings using the soup object if found
def getProductRatings(soup):
    try:
        product_ratings = soup.find('span', attrs = {'class' : 'a-icon-alt'})   # This statement will find the
                                                                                # product ratings from the web page
                                                                                # whose is hidden in span element
                                                                                # of class    'a-icon-alt'
        prd_ratings = product_ratings.text.strip()
    except:
        return ""
    return prd_ratings


# Method which will return the product availability and seller name if product is
# available using the soup object if found
def getSellerNameIFNotOutOfStock(soup):
    stock_status = True
    seller_name = ""
    try:
        div = soup.find('div', attrs = {'id' : 'availability'})                             # This will traverse the div element content using
                                                                                            # find method whose id is 'availability'
                                                                                            # To check whether the stock is available or not
        if (div.find('span').text.strip() in ['In stock', 'in stock', 'IN STOCK']):         # If the stock is available than the seller name is fetched
            merchant_info = soup.find('div', attrs = {'id' : 'merchant-info'})              # which is hidden in nested div element with id 'merchant-info'
            seller_name = merchant_info.find('a').find('span').text.strip()

    except:
        stock_status = False
        return ""

    if (stock_status):
        return seller_name
    else:
        return "Seller not available " + div.find('span').text.strip()  # If Stock Status is out of stock then the exception will be returned

# Main method which contains the navigating the links selenium and creating the soap objects using beautiful soap
# to scrap the amazon website data
def main():

    url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"   # Setting the given url for the project

    chrome_options = Options()                                                  # Initializing the chrome options object to disable the gui opening
    chrome_options.add_argument("--headless")                                   # Setting the option as --headless to avoid opening of GUI on get() of selenium
    driver = webdriver.Chrome(options=chrome_options)                       # Setting the web driver chrome with option for avoiding the GUI opening

    driver.get(url)                                                         # Navigating the url using get() of selenium
    html_content = driver.page_source                                       # Fetching the HTML content of the url using the page_source property

    soup = BeautifulSoup(html_content, 'html.parser')                       # Parsing the html content using the html.parser

    elems = soup.find(class_="sg-col-20-of-24 s-matching-dir sg-col-16-of-20 sg-col sg-col-8-of-12 sg-col-12-of-16")    # Finding the element for the result product page which will have all the products links in it

    link = "https://amazon.in"
    links = []
    data = {"Product_Name" : [], "Product_Price" : [], "Product_Ratings" : [], "Seller_Name(IF not Out of Stock)" : [] }   # Taking the dictionary data structure to put it in csv file
    for divs in elems.contents:
        for nested_divs in divs.find_all('div'):                # Iterating the nested div elements
            if (nested_divs.find('a') is not None):
                a = nested_divs.find('a')
                links.append(link + a.get('href'))              # Putting the links of the product results using the a.get('href') and concatenating with the url that is link for preffix
    links = set(links)
    finallinks = list(links)                            # Stored all the product links

    i = 0

    # Iterating to each product link and fetching the required product information from the product links
    for a_links in finallinks:
        print(f"Fetching Product {i+1} Details...")
        if a_links != "https://amazon.injavascript:void(0)":

            driver.get(a_links)
            html_source = driver.page_source
            new_soup = BeautifulSoup(html_source, 'html.parser')
            data['Product_Name'].append(getProductDetails(new_soup))
            data['Product_Price'].append(getProductPrice(new_soup))
            data['Product_Ratings'].append(getProductRatings(new_soup))
            data['Seller_Name(IF not Out of Stock)'].append(getSellerNameIFNotOutOfStock(new_soup))

        i += 1
    driver.quit()           # Quiting the browser chrome

    # Storing the data in .csv formate using pandas dataframe
    amazon_dataFrame = pd.DataFrame.from_dict(data)
    # Replacing the empty product name with the NULL values if product name not found
    amazon_dataFrame['Product_Name'].replace('', np.nan, inplace = True)
    amazon_dataFrame = amazon_dataFrame.dropna(subset = ['Product_Name'])
    amazon_dataFrame.to_csv('amazon_product_data.csv', header = True, index = False)

    # Product details scraping task done successfully !!!
main()

