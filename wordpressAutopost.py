##Import libraries and packages for the project
import random
import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import requests
from requests.auth import HTTPBasicAuth
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv

def concatenate_and_newline(input_list):
    result = '\n'.join(map(str, input_list))
    return result

# Replace these values with your WordPress site information
wordpress_url = 'https://thesissupporthub.com/wp-json/wp/v2/posts'
username = 'Brian'
password = 'hsLv EKB2 whZt gkoZ TBDA oQQP'

driver = webdriver.Chrome()
sleep(2)

url = 'https://www.sweetstudy.com/fields/information-systems?page=15'
driver.get(url)
sleep(2)

driver.maximize_window()

numberofPages = int(input("Please enter the number of pages you want to mine: "))
page_source = BeautifulSoup(driver.page_source, "html.parser")

topicList = []
questionsList = []
titleList = []

count = 0
pageCount = 0

for presentpage in range(numberofPages):
    try:
        topics = page_source.find_all('a', class_ = 'css-e5w42e')
        topicList.append(topics)
        print("The number of topics mined is: ", len(topics))

        for topic in topics:
            try:
                topicLink = topic.get('href')
                topicURL = "https://www.sweetstudy.com" + topicLink
                driver.get(topicURL)
                sleep(3)

                page_source2 = BeautifulSoup(driver.page_source, "html.parser")
                try:
                    title = page_source2.find('div', class_ = 'css-8fqqpo').getText().strip()
                except:
                    pass
                try:
                    questions = page_source2.find_all('div', class_ ='css-1lys3v9')
                except:
                    pass
                try:
                    titleList.append(title)
                except:
                    pass

                for question in questions:
                    try:
                        questionsList.append(question.get_text().strip())
                    except:
                        pass
                try:
                    concatenated_questions = concatenate_and_newline(questionsList)
                except:
                    pass
                # Post data
                post_data = {
                    "title": title,
                    "content": concatenated_questions,
                    "status": "publish"
                }

                # Make the request to create a new post
                response = requests.post(
                    wordpress_url,
                    auth=HTTPBasicAuth(username, password),
                    json=post_data
                )

                # Check the response
                if response.status_code == 201:
                    print("Post created successfully!")
                    print("Post ID:", response.json()["id"])
                else:
                    print("Failed to create post. Status code:", response.status_code)
                    print("Error message:", response.text)
            except:
                pass

        pageCount = pageCount + 1

        if numberofPages == pageCount:
            pass
        else:
            driver.get(f"https://www.sweetstudy.com/fields/information-systems?page={presentpage+16}")

    except:
        pass

print("Successfully extracted the pages")









