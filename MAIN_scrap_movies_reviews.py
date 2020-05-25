from selenium import webdriver
import urllib.request as url
import bs4
import time
def reviews_extract():
    movie = input('Enter name of movie:')
    movie = movie.lower()

    web = url.urlopen("https://www.imdb.com/find?ref_=nv_sr_fn&q="+movie)
    page1 = bs4.BeautifulSoup(web,'lxml')
    b = page1.find('td',class_='result_text')
    href = b.a['href']
    web2 = url.urlopen("https://www.imdb.com"+href)
    page2 = bs4.BeautifulSoup(web2,'lxml')
    c = page2.find('div',class_='user-comments')
    temp = []
    for a in c.find_all('a',href =True):
        g =(a['href'])
        temp.append(g)
    d = temp[-1]
    driver = webdriver.Chrome('C:\\Users\\dell\\Desktop\\chromedriver.exe')
    driver.get("https://www.imdb.com"+d)
    for i in range(20):
        try:
            loadMoreButton = driver.find_element_by_class_name('load-more-data')
            loadMoreButton.click()
            time.sleep(1)
        except Exception as e:
            print(e)
            break
    web3 = driver.page_source
    page3 = bs4.BeautifulSoup(web3,'lxml')

    e = page3.find('div',class_='lister-list')

    e1 = e.find_all('a',class_='title')

    user_reviews = []
    for i in e1:
        raw = (i.text)
        user_reviews.append(raw.replace('\n',''))
    driver.quit()
    print(user_reviews)
    print(len(user_reviews))
    return user_reviews,movie

#reviews()


