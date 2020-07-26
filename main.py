import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys

data = {
    'notas': [],
    'comentarios': []
}

def getRating(driver):
    div_data = driver.find_elements_by_class_name('rating-evaluation__wrapper')
    for evaluation in div_data:
        innerHTML = evaluation.get_attribute('innerHTML')
        soup = BeautifulSoup(innerHTML, 'html.parser')
        comment_user = soup.findAll('p', {'class': 'rating-evaluation__user'})
        if len(comment_user) > 0 :
            rating_user = soup.findAll('span', {'class': 'rating-evaluation-header__rate'})
            data['notas'].append(rating_user[0].text)
            data['comentarios'].append(comment_user[0].text)


def listRestaurants():   
    list_elements = driver.find_elements_by_class_name('restaurant-card__wrapper')
    hrefs = list()

    
    for elem in list_elements:
        hrefs.append(elem.get_attribute('href'))
    
    for elem in hrefs:
        driver.get(elem)
        time.sleep(3)

        try:
            modalTakeOut = driver.find_element_by_class_name('takeout-app-modal__button-ok')
            modalTakeOut.click()

        except:
            print(sys.exc_info()[0])

        try:
            btn_rating = driver.find_element_by_class_name('restaurant-rating__button')
            btn_rating.click()
            getRating(driver)
        except:
            print(sys.exc_info()[0])

    count = len(list_elements)

        
if __name__ == "__main__":
    url = 'https://www.ifood.com.br/lista-restaurantes'
    
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)

    modalUseMyLocation = driver.find_element_by_class_name('btn-address--full-size')
    modalUseMyLocation.click()
    time.sleep(3)

    countRestaurants = 0
    loadMore = True
    while loadMore:
        listRestaurants(countRestaurants)
        try:
            btnLoadMore = driver.find_element_by_class_name('restaurants-list__load-more')
        except:
            loadMore = False
            print(sys.exc_info()[0])
            


    
    
        