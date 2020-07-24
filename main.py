import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys

data = {
    'notas': [],
    'comentarios': []
}

def getrating(driver):
    div_data = driver.find_elements_by_class_name('rating-evaluation__wrapper')
    for evaluation in div_data:
        innerHTML = evaluation.get_attribute('innerHTML')
        soup = BeautifulSoup(innerHTML, 'html.parser')
        comment_user = soup.findAll('p', {'class': 'rating-evaluation__user'})
        if len(comment_user) > 0 :
            rating_user = soup.findAll('span', {'class': 'rating-evaluation-header__rate'})
            data['notas'].append(rating_user[0].text)
            data['comentarios'].append(comment_user[0].text)
        
if __name__ == "__main__":
    url = 'https://www.ifood.com.br/delivery/sao-caetano-do-sul-sp'
    # page = requests.get(url)
    # soup = BeautifulSoup(page.text, 'html.parser')
    
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    list_elements = driver.find_elements_by_class_name('restaurant-card__wrapper')
    # for elem in list_elements:
    list_elements[0].click()
    time.sleep(3)
    try:
        modal = driver.find_element_by_class_name('takeout-app-modal__button-ok')
        modal.click()
    except:
        print(sys.exc_info()[0])

    try:
        btn_rating = driver.find_element_by_class_name('restaurant-rating__button')
        btn_rating.click()
        getrating(driver)
    except:
        print(sys.exc_info()[0])
    print('teste')