from bs4 import BeautifulSoup
import requests
import urllib2
import os
import errno
import json
import time
import random

def getDoi(year,issue,page):
 #year = '45'
 #issue = 'D1'
 time.sleep(random.randint(1,30))
 page = '1'
 foldername = 'year'+year
 response = requests.post("https://wrapapi.com/use/sjn/testoup/oup/0.0.7", json={
   "year": year,
   "issue": issue,
   "page": page,
   "wrapAPIKey": "8X6fUU7zDvhD0I8M7AXGDbj5yK4sT8xX"
 })
 # json_data = json.loads(response.text)
 # print json_data

 jason_data = response.json()
 #print (jason_data['data']['DOIs'][0])
 DOIs = []
 time.sleep(random.randint(5,30))
 for doi in jason_data['data']["DOIs"]:
   print (doi.split("\'")[0])
   url = doi.split("\'")[0]
   DOIs.append(url)

 abstracts = []
 titles = []
 authors = []
 try:
     os.makedirs(foldername)
 except OSError as e:
     if e.errno != errno.EEXIST:
         raise
 for url in DOIs:
   try:
     time.sleep(random.randint(1,30))
     headers = {'User-Agent': 'Mozilla/5.0'}
     request = urllib2.Request(url, headers=headers)
     page = urllib2.urlopen(request).read()

     soup = BeautifulSoup(page, features="html.parser")
     save_data = {}

     #print soup.body
     is_captcha_on_page = soup.find(attrs={'class': 'abstract'}) is None
     if is_captcha_on_page:
       print ("ERROR: Captcha showed up!")
     
     abstract = soup.find(attrs={'class': 'abstract'}).p
     title = soup.find(attrs={'class': 'article-title-main'})
     authors = soup.select(".linked-name")
     abstracts.append(abstract)
     titles.append(title)
     ld_json_data_str = soup.find('script', {'type': 'application/ld+json'}).text.encode('utf-8')
     ld_json_data = json.loads(ld_json_data_str)
     
     if("keywords" in ld_json_data):
         keywords = ld_json_data['keywords']
     if("about" in ld_json_data):
         about = ld_json_data['about']

     uniqueIdentifier = url[url.rfind('/')+1:]
     filename = foldername + '/' + uniqueIdentifier + ".json"
    
     save_data['title'] = title.text.encode('utf-8')
     save_data['abstract'] = abstract.text.encode('utf-8')
     save_data['authors'] = authors.text.encode('utf-8')
     if('keywords' in ld_json_data):
         save_data['keywords'] = ld_json_data['keywords']
     if('about' in ld_json_data):
         save_data['about'] = ld_json_data['about']

     print(uniqueIdentifier)
     with open(filename, 'w') as file:
      # file.write(title.text.encode('utf-8'))
       json.dump(title, file)
        
   except IOError as e:
     # print(e.errno)
     # print(e)
     print (url+" NOT PROCESSED! (No Abstract Found)")

if __name__ == "__main__":
    for i in range(34,40):
        getDoi(str(i),"suppl_1","1")

 
