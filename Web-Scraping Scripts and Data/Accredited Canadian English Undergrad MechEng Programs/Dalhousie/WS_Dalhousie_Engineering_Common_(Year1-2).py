from bs4 import BeautifulSoup as soup
from selenium import webdriver
import time
import re
import pandas as pd

url = 'https://academiccalendar.dal.ca/Catalog/ViewCatalog.aspx?pageid=viewcatalog&catalogid=111&chapterid=6729&loaduseredits=False'

#set up selenium webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
#chrome_options.add_argument('--headless')

driver = webdriver.Chrome("C:\\Users\\jerry\\Downloads\\chromedriver", options=chrome_options)
time.sleep(5)

#go to course list page
driver.get(url)
time.sleep(3)

#find all course code links that link to course info page
link_texts = re.findall("[A-Z]{4} [0-9]{4}", driver.page_source)
link_texts = list(dict.fromkeys(link_texts)) #remove duplicates

course_codes = []
course_names = []
course_descs = []
counter = 0

#begin scraping
for link_text in link_texts[::-1]: #when links are clicked from top to bottom some overlapping occurs in the links that lead to errors. So click links from bottom to top
    
    #go to course webpage
    link = driver.find_element_by_link_text(link_text)
    time.sleep(2)
    link.click()
    time.sleep(3)
    page_source = driver.page_source
    
    #handoff to beautiful soup
    page_soup = soup(page_source, 'lxml')
    container = page_soup.find("div", {"class": "maincontent"})
    
    course_code = container.find("b").text.split("\xa0\xa0")[0].strip()
    course_name = container.find("b").text.split("\xa0\xa0")[1].strip()
    
    texts = re.split(r'\n+', container.text)
    texts = [text for text in texts if (len(text)>5) and ("REQUISITES:" not in text) and ("FORMAT" not in text)]
    
    #assume the course description is the longest string in the texts list
    course_desc = max(texts, key = len).strip()
    
    course_codes.append(course_code)
    course_names.append(course_name)
    course_descs.append(course_desc)
    
    print("Scraped ", course_code)
    counter += 1
    
    #go back to course list webpage
    driver.back()
    time.sleep(3)

print("Finished scraping {} courses".format(counter))

#reverse the lists for chronological order
course_codes = course_codes[::-1]
course_names = course_names[::-1]
course_descs = course_descs[::-1]

#organize as dataframe and write to csv file
df = pd.DataFrame({
    
    "Course Number": course_codes,
    "Course Name": course_names,
    "Course Description": course_descs
})

df.to_csv('Dalhousie_Engineering_Common_(Year1-2)_Courses.csv', index = False)

driver.quit()