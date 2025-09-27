#Image Site Downloader
#Currently working for Imgur

import requests, time, sys, bs4, os
import pyinputplus as pyip

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

image_url = pyip.inputStr(prompt = 'Enter the website url:\n')

category = pyip.inputStr(prompt = 'Enter a category to search:\n')

#Maximum photos to download
max_photos = 50

search_url = ''

#Start Firefox browser
browser = webdriver.Firefox()

#Go to webpage
browser.get(image_url)

#Imgur consent button click
try:
    #Wait at least 10 seconds for element to appear
    consent_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.fc-cta-consent'))
    )
    
    time.sleep(0.5) #crapa daca nu astepti

    consent_element.click() #crapa daca e cu ''

except Exception:
    raise Exception

def search_with_bar(css_sel):
    search_element = browser.find_element(By.CSS_SELECTOR, \
                                          css_sel)

    search_element.send_keys(category) #crapa daca e cu ''

    search_element.send_keys(Keys.ENTER)

try:
    #Wait at least 10 seconds for element to appear
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id*="earch"]')) #Flickr search bar
    )
except Exception:
    try:
        #Wait at least 10 seconds for element to appear
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(\
                (By.CSS_SELECTOR, 'input[class*="earch"]'))) #Imgur search bar
    except:
        raise Exception
    else:
        time.sleep(0.5) #crapa daca nu nu astepti
        #Search for keyword and enter
        search_with_bar('input[class*="earch"]')
else:
    time.sleep(0.5) #crapa daca nu astepti
    #Search for keyword and enter
    search_with_bar('input[id*="earch"]')
finally:
    time.sleep(1)
    #Get current url
    search_url = browser.current_url
    browser.quit()

#Download result page with requests
res = requests.get(search_url, headers = {'User-agent': 'your bot 0.1'})

res.raise_for_status()

#Make dir where to put photos
os.makedirs(category, exist_ok=True)

#Parse html page with bs4
noStarchSoup = bs4.BeautifulSoup(res.text, 'html.parser')

#Search for all image elements
img_elems = noStarchSoup.select('img')

if img_elems == []:
    print('Could not find any image.')
else:
    #Download maximum 50 photos
    counts = min(max_photos, len(img_elems))
    for index in range(counts):
        img_url = 'https:' + img_elems[index].get('src')
        # Download the image.
        print('Downloading image %s...' % (img_url))
        res = requests.get(img_url, headers = {'User-agent': 'your bot 0.1'})
        res.raise_for_status()
        #Save file image
        imageFile = open(os.path.join(category, os.path.basename(img_url)), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()
    print('No. images:' + str(counts) + '. Done.')
    

