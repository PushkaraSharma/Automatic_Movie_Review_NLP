from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import urllib.request as url
import bs4
import time
def reviews_extract():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=r'/home/pushkarasharma/Automatic_Movie_Review_NLP/chromedriver', chrome_options=options)
   
    movie = input('Enter name of movie:')
    movie = movie.lower()
   
    web = url.urlopen("https://www.imdb.com/find?ref_=nv_sr_fn&q="+movie)
    page1 = bs4.BeautifulSoup(web,'lxml')
    b = page1.find('td',class_='result_text')
    href = b.a['href']
    pageUrl = "https://www.imdb.com"+href+"reviews?ref_=tt_urv"
    print(pageUrl)
    
    driver.get(pageUrl)
    for i in range(20):
        try:
            loadMoreButton = driver.find_element_by_class_name('ipl-load-more__button')
            driver.implicitly_wait(2)
            loadMoreButton.click()
            print("click")
            time.sleep(2)
        except Exception as e:
            print(e)
            break

    web2 = driver.page_source
    page2 = bs4.BeautifulSoup(web2,'lxml')
    c = page2.find('div',class_='lister-list')
    user_reviews = []

    for a in c.find_all("div", class_="content"):
        g =a.text
        user_reviews.append(g.replace('\n',''))

    driver.quit()
    
    print(user_reviews)
    print(len(user_reviews))
    return user_reviews,movie


