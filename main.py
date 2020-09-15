import requests
import time
import sys
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

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
    try:
        for target_list in range(0, 30):
            btnLoadMore = driver.find_element_by_class_name('restaurants-list__load-more')
            btnLoadMore.click()
            time.sleep(3)
    except:
        print(sys.exc_info()[0])

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


def inputAddress(adrress):
    btnInputLocation = driver.find_element_by_class_name('address-search-input__button')
    btnInputLocation.click()
    time.sleep(3)
    inputLocation = driver.find_elements_by_class_name('address-search-input__field')
    inputLocation[1].send_keys(adrress + ', São Paulo')
    time.sleep(3)

    listAddress = driver.find_element_by_class_name('address-search-list')
    listItem = listAddress.find_elements_by_tag_name('li')
    listItem[0].click()
    time.sleep(3)

    try:
        formNumberInput = driver.find_element_by_class_name('address-number__form')
        checkAddressNoNumber = formNumberInput.find_element_by_id('addressEmptyNumber')
        checkAddressNoNumber.click()
        time.sleep(1)
        btnSearchWithoutNumber = formNumberInput.find_element_by_class_name('btn--full-width')
        btnSearchWithoutNumber.click()
        time.sleep(3)
    except:
        print(sys.exc_info()[0])

    btnConfirmAddress = driver.find_element_by_class_name('address-maps__submit')
    btnConfirmAddress.click()
    time.sleep(3)

    divSaveAddress = driver.find_element_by_class_name('complete-address--save-btn')
    btnSaveAddress = divSaveAddress.find_element_by_class_name('btn--full-width')
    btnSaveAddress.click()
    time.sleep(3)

if __name__ == "__main__":
    url = 'https://www.ifood.com.br/lista-restaurantes'
    
    chromeOptions = webdriver.ChromeOptions()
    # chromeOptions.add_argument("--kiosk");
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    dfDistrict = pd.read_csv("./district.csv")

    driver.get(url)
    time.sleep(3)
    inputAddress(dfDistrict['District'][0])    
    listRestaurants()

    

    for district in dfDistrict['District'][1:]:
        driver.get(url)
        time.sleep(3)
        btnChangeAddress = driver.find_element_by_class_name('delivery-input')
        btnChangeAddress.click()
        time.sleep(2)
        inputAddress(district)    
        listRestaurants()



    df = pd.DataFrame.from_dict(data)
    compression_opts = dict(method='zip',
                        archive_name='out.csv')  
    df.to_csv('out.zip', index=False,
              compression=compression_opts)     
    
        