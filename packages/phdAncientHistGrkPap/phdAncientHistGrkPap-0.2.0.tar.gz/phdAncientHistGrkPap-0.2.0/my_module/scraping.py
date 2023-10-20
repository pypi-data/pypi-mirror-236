import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import time
import random

def fetch_from_pinfo(url,target):
    res=requests.get(url)
    soup=bs(res.text,'html.parser')
    for row in soup.find_all('tr'):
        h_cells = row.find_all('th')
        for hc in h_cells:
            if hc.text.strip()==target:
                dc=hc.find_next_sibling('td')
                if dc:
                    return dc.text.strip()
    return None

def scaled_fetch(tm_id_list,target,t1,t2):
    url1 = 'https://papyri.info/trismegistos/'
    out=[]
    for el in tm_id_list:
        url2=url1+str(el)
        out.append(fetch_from_pinfo(url2,target))
        time.sleep(random.uniform(t1,t2))
    return out