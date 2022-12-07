#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup


# In[2]:


years = [1930, 1934, 1938, 1942, 1946, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 
         1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018]


# In[3]:


url = "https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup"


# In[4]:


import requests
response = requests.get(url)
response.text


# In[5]:


content = response.text
soup = BeautifulSoup(content, "lxml")


# In[6]:


soup.find_all("h2")


# ### Testing with 2014

# In[7]:


# List of all matches
matches = soup.find_all("div", class_="footballbox") # where div is the tag

home = []
score = []
away = []

for match in matches:
    home.append(match.find("th", class_="fhome").get_text())
    score.append(match.find("th", class_="fscore").get_text())
    away.append(match.find("th", class_="faway").get_text())
    
# Create a dictionary
fifa_dict = {"home":home, "score":home, "away":away}

#Create a df
fifa_df = pd.DataFrame(fifa_dict)
fifa_df["year"] = "2014"
fifa_df.head()


# ### Every year since 1930

# In[8]:


def get_matches(year):
    url = f"https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup"
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, "lxml")
    # List of all matches
    matches = soup.find_all("div", class_="footballbox") # where div is the tag

    home = []
    score = []
    away = []

    for match in matches:
        home.append(match.find("th", class_="fhome").get_text())
        score.append(match.find("th", class_="fscore").get_text())
        away.append(match.find("th", class_="faway").get_text())
    
    # Create a dictionary
    fifa_dict = {"home":home, "score":score, "away":away}

    #Create a df
    fifa_df = pd.DataFrame(fifa_dict)
    fifa_df["year"] = year
    return fifa_df
get_matches(2018)


# * For some years, we can't extract all data because of difference in html

# In[9]:


all_fifa = [get_matches(year) for year in years]
fifa = pd.concat(all_fifa, ignore_index = True)
fifa.to_csv("fifa_world_cup_historical_data.csv",index = False)


# ### 2022 World Cup Fixtures

# In[10]:


fixture_df = get_matches(2022)
fixture_df.to_csv("fifa_2022_world_cup_fixtures.csv", index = False)


# In[ ]:




