# Adding the dependencies for the project to scarp the given information :- bio, following count,
# followers count, location, website of a specific user from twitter website
# And store it into the Mysql Database

import csv
import mysql.connector as mysql

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



# Function to scrap BIO of a user from twitter website using XPATH
# for the element in which bio content is hidden or written
def getUserBio(driver, bioXPATH):
    try:
        #Setting  up a WebDriverWait with a timeout of 10 seconds.
        # This will be used to wait for a specific condition to be met.
        # In this case, the condition is the visibility of an element.

        b_content = WebDriverWait(driver, 10).until(
            # Specifying the condition for WebDriverWait.
            # Here, the condition is the visibility of an element located by its XPath.
            EC.presence_of_element_located(
                (By.XPATH,
                 bioXPATH)
            )
        )
        user_bio = b_content.text               # If the element is visible within the timeout period,
                                                # then return user_bio


    except:
        print("Couldn't fetch the User's Bio")   # If element not found by XPATH then raising exception
        return ""
    return user_bio



# Function to scrap the User's following counts from the twitter website using the XPATH
# for the element in which following count content is written
def getUserFollowingCount(driver, followingXPATH):
    try:
        # This will be used to wait for a specific condition to be met.
        # In this case, the condition is the visibility of an element.
        # This will be for the element which is scrapped with the provided XPATH

        fll_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 followingXPATH)
            )
        )
        user_following_count = fll_content.text

    except:
        print("Couldn't fetch the User's following counts")
        return ""
    return user_following_count



# Function to scrap the User's followers count from twitter website using XPATH
# for that element in which user's followers count is written or hidden in that element
def getUserFollowersCount(driver, followersXPATH):
    try:
        fllrs_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 followersXPATH)
            )

        )
        user_followers_count = fllrs_content.text

    except:
        print("Couldn't fetch the User's followers counts")
        return ""

    return user_followers_count



# Function to scrap the User's Location from the twitter website using XPATH
# for the element in which location information is written
def getUserLocation(driver, locationXPATH):
    try:
        l_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 locationXPATH)
            )
        )
        user_location = l_content.text
    except:
        print("Couldn't fetch the User's location")
        return ""

    return user_location



# Function to scrap the User's website from the twitter if available using XPATH
# for the element in which website text or url of the website is written
def getUserWebsite(driver, websiteXPATH):
    try:
        w_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 websiteXPATH)
            )
        )
        user_website = w_content.text

    except:
        print("Couldn't fetch the User's website")
        return ""

    return user_website



# Function to fetch the links from the twitter_links.csv file
def getLinksFromFile():
    try:

        with open("twitter_links.csv","r") as file:     # Opening file twitter_links.csv to fetch the
                                                        # urls of the twitter

            r_obj = csv.reader(file)                    # Creating a csv reader object to read the content
                                                        # from the twitter_links.csv file

            data_links = []                             # Taking list to store all the urls fetched
                                                        # from the twitter_links.csv file
            for links in r_obj:
                data_links.append(links)                # Storing the urls in the list


    except Exception as E:                  # Raising the exception if the file is not found
        print(E)
        return ""
    return data_links                   # Returning the fetched urls to the function head

## Function to insert the scrapped data into the database mysql table
def insertDataToTabel(cursor_obj , bio_data, following_count, followers_count, location, website):
    try:
        ## Inserting the scrapped information into the table...

        query = "INSERT INTO Twitter_Details VALUES (%s, %s, %s, %s, %s)"
        values = (bio_data, following_count, followers_count, location, website)
        cursor_obj.execute(query, values)
    except Exception as e:
        print(f"Error inserting data: {e}")



## Function to fetch the scrapped data from the database table... Twitter_details


def fetchDataFromDatabaseTable(cursor_obj):
    cursor_obj.execute('select * from Twitter_Details')
    records = cursor_obj.fetchall()
    for record in records:
        print(record)
    cursor_obj.execute('truncate table Twitter_Details')


# Function to navigate to the links which is being fetched from the file :- twitter_links.csv.

def navigatingLinks(urls):
    # Setting up the Mysql Connection
    con_obj = mysql.connect(host = 'localhost', user = 'root', password = 'devpatel')

    # Initialising the Cursor Object
    cur_obj = con_obj.cursor()

    # Creating the Database
    cur_obj.execute('create database if not exists Twitter_Scrapped_Details')

    # Opening the Database
    cur_obj.execute('use Twitter_Scrapped_Details')

    # Creating the table to store the scrapped data
    cur_obj.execute("""
        CREATE TABLE IF NOT EXISTS Twitter_Details (
            User_Bio VARCHAR(200) PRIMARY KEY,
            `Following Count` VARCHAR(15),
            `Followers Count` VARCHAR(15),
            Location VARCHAR(80),
            Website VARCHAR(20)
        )
    """)


    chrome_options = Options()                                                  # Initializing the chrome options object to disable the gui opening
    chrome_options.add_argument("--headless")                                   # Setting the option as --headless to avoid opening of GUI on get() of selenium
    driver = webdriver.Chrome(options=chrome_options)                       # Setting the web driver chrome with option for avoiding the GUI opening





    # Setting up the XPATH's for Bio, Following Count, Followers Count,
    # Location and Website (if available)

    bioXPATH = "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div"
    followingXPATH = "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span"
    followersXPATH = "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span"
    locationXPATH = "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div/span[1]/span/span"
    websiteXPATH = "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[4]/div/a/span"

    for t_links in urls:                                        # Navigating to the urls
        for link in t_links:
            print(link)
            driver.get(link)
            print("----------------------------------------------------------------------------")

            # Calling the functions which are defined above for bio, following count, followers count,
            # location and website and passing two arguments namely driver object and the XPATH for
            # specific information

            bio = getUserBio(driver, bioXPATH)
            following_count = getUserFollowingCount(driver, followingXPATH)
            followers_count = getUserFollowersCount(driver, followersXPATH)
            location = getUserLocation(driver, locationXPATH)
            website = getUserWebsite(driver, websiteXPATH)
            if (bio and following_count and followers_count and location and website):  # If all information is available on the website and successfully scrapped

                print(f"Successfully scrapped the given information of {link} !!! ")
            else:
                print(f"Scrapped the few information of {link} !!! ")
            if (bio=='' and following_count == '' and followers_count=='' and location=='' and website==''):
                pass
            else:


                # Function to insert the scrapped information into the database table
                insertDataToTabel(cur_obj, bio, following_count, followers_count, location, website)




    driver.quit()       # Quiting the browser chrome

    con_obj.commit() # Saving/Committing the data into the table

    fetchDataFromDatabaseTable(cur_obj)







urls = getLinksFromFile()                   # Passing the urls fetched and stored into list to the
                                            # navigatingLinks() to navigate the links which are stored
                                            # in a list

navigatingLinks(urls)                       # Passing the list of urls to the function as actual parameters
