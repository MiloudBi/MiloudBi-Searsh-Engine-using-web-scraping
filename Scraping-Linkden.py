#!/usr/bin/env python
# coding: utf-8

# In[77]:


#imports
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import TimeoutException
import os, random, sys, time
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import re
import nltk  
from selenium.webdriver.common.action_chains import ActionChains
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
import numpy as np 


# In[78]:


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")


# In[79]:


# defining new variable passing two parameters
file = open('C:/Users/SefianiMiloud/Desktop/config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]

# specifies the path to the chromedriver.exe
driver = webdriver.Chrome('C:/Users/SefianiMiloud/Desktop/chromedriver',options=options)

# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com/uas/login')

# locate email form by_class_name
elementID = driver.find_element_by_id('username')

# send_keys() to simulate key strokes
elementID.send_keys(username)

# locate password form by_class_name
elementID = driver.find_element_by_id('password')

# send_keys() to simulate key strokes
elementID.send_keys(password)

# locate submit button by_xpath
sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

# .click() to mimic button click
sign_in_button.click()


# In[80]:


fullLink = 'https://www.google.com/'
driver.get(fullLink)
# locate search form by_name
search_query = driver.find_element_by_name('q')

# send_keys() to simulate the search text key strokes
search_query.send_keys('site:linkedin.com/in/ AND "Business Intelligence" AND "Maroc" AND "open to work"')

# .send_keys() to simulate the return key 
search_query.send_keys(Keys.RETURN)
time.sleep(5)


# In[81]:


links=[]
elems=[]
for nb in range(15):
    elems = driver.find_elements_by_xpath('//*[@id="search"]//a[starts-with(@href, "https://ma.linkedin.com/")]')
    for elem in elems:
        print(elem)
        my_href = elem.get_attribute("href")
        links.append(elem.get_attribute("href"))
    Next_Google_page = driver.find_element_by_link_text("Next").click()
time.sleep(2)
    # perform your tasks in the new window and switch back to the parent windown for the remaining hrefs


# In[82]:


print(links)
print(len(links))
   


# In[83]:


def scroll_to_bottom(driver):

    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))

scroll_to_bottom(driver)


# In[84]:


def convert(match_experience): 
    return (match_experience.split()) 


# In[86]:


import heapq
import csv
A=open('C:/Users/SefianiMiloud/Desktop/ete.csv')
lines = A.readlines()
info=[]
for url in links:
    data={}
    urls = "'"+url+"'"
    print("url=",urls,'\n')
    data["url"]=url
    driver.get(url)
    time.sleep(5)
    source=driver.page_source
    soup = BeautifulSoup(source,'lxml')
    name_div=soup.find('div', {'class': 'flex-1 mr5'})
    name_loc=name_div.find_all('ul')
    name =name_loc[0].find('li').get_text().strip()
    print("name=",name)
    data["name"]=name
    localisation =name_loc[1].find('li').get_text().strip()
    print("localisation=" ,localisation)
    data["localisation"]=localisation
    profile_title=name_div.find('h2').get_text().strip()
    print("profile_title=",profile_title)
    data["profile_title"]=profile_title
    #job of profil
    try:
        exp_section=soup.find('section',{'id':'experience-section'})
        containers1 = exp_section.find_all("h3",{"class":'t-16 t-black t-bold'})
        job_title=[]
        for test in containers1:
                 print(test.get_text().strip())
                 job_title.append(test.get_text().strip())
        data["job_title"]=job_title
    except AttributeError as e:
        data["job_title"]=None
     ##company name 
    try:
        li_tags=exp_section.find_all("p",{"class":"pv-entity__secondary-title t-14 t-black t-normal"})
    
        company_name=[]
        for test1 in li_tags:
                print(test1.get_text().strip())
                company_name.append(test1.get_text().strip())
        data["company_name"]=company_name
    except AttributeError as e:
        data["company_name"]=None    
    ##joining_date
    try:
        joining=exp_section.find_all("h4",{"class":"pv-entity__date-range t-14 t-black--light t-normal"})
    
        joining_date=[]
        for te in joining:
                print(te.find_all('span')[1].get_text().strip())
                joining_date.append(te.find_all('span')[1].get_text().strip())
        data["joining_date"]=joining_date
    except AttributeError as e:
        data["joining_date"]=None
        #duration
    try:
        li_ta=exp_section.find_all("span",{"class":"pv-entity__bullet-item-v2"})
   
        duration=[]
        for  t in li_ta:
                print(t.get_text().strip())
                duration.append(t.get_text().strip())
        data["duration"]=duration
    except AttributeError as e:
        data["duration"]=None
     #nltk experience
    try:
        containers = exp_section.find_all("p",{"class":'pv-entity__description t-14 t-black t-normal inline-show-more-text inline-show-more-text--is-collapsed ember-view'})     

        article_text = ''
        for para in containers:  
                article_text += para.text
        newString = article_text.replace('see more', '')
        corpus = nltk.sent_tokenize(newString)
        for i in range(len(corpus )):
            corpus [i] = corpus [i].lower()
            corpus [i] = re.sub(r'\W',' ',corpus [i])
            corpus [i] = re.sub(r'\s+',' ',corpus [i])
        wordfreq = {}
        for sentence in corpus:
            tokens = nltk.word_tokenize(sentence)
            for token in tokens:
                if token not in wordfreq.keys():
                    wordfreq[token] = 1
                else:
                    wordfreq[token] += 1
        most_freq = heapq.nlargest(200, wordfreq, key=wordfreq.get) 
        converted_lines = []
        for element in lines:
            converted_lines.append(element.strip())
        match_experience=' '.join(list(set(most_freq) & set(converted_lines)))
        match_experiences=convert(match_experience)
        data["match_experiences"]=match_experiences
    except AttributeError as e:
        data["match_experiences"]=None
    scroll_to_bottom(driver)
    try:  
        driver.execute_script("arguments[0].scrollIntoView(true);", WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[@aria-controls='skill-categories-expanded' and @data-control-name='skill_details']/span[normalize-space()='Show more']"))))
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-controls='skill-categories-expanded' and @data-control-name='skill_details']/span[normalize-space()='Show more']"))))
        time.sleep(5)
    except TimeoutException:
            pass
           
    try:
        list_skills=[]
        source=driver.page_source
        soup = BeautifulSoup(source,'lxml')
        all_skills=soup.find_all('span',{'class':'pv-skill-category-entity__name-text t-16 t-black t-bold'})
        for slill in all_skills:
            print(slill.get_text().strip())
            list_skills.append(slill.get_text().strip())
        data["list_skills"]=list_skills     
    except AttributeError as e:
        data["list_skills"]=None          
    info.append(data)    
    driver.forward()
        

    
  


# In[87]:


info


# In[88]:


import json
with open('Scraping_linkdeln_Data.json', 'a+', encoding='utf-8') as outfile:
        array = {'profils_linkden': info }
        foo_list = array['profils_linkden']
        for line in outfile:
            obj = json.loads(line)
            foo_list.append(obj)
        outfile.write(json.dumps(array, indent=2, separators=(',', ': ')))
        outfile.write('\n')
       

