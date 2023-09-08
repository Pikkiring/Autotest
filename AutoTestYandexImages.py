
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from urllib.parse import unquote
import hashlib
import shutil
import requests


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
browser = webdriver.Chrome(chrome_options)


link = "https://ya.ru/"
required_url = 'https://ya.ru/images/'

##Xpaths:
checkbot_xpath = '//input[@class="CheckboxCaptcha-Button"]'
search_string_xpath = '//input[contains(@class ,"search3__input")]'
button_menu_xpath = '//div[@class="services-suggest__icons-more"]'
button_img_xpath = '//a[@aria-label="Картинки"]'
whole_images_categories_xpath = '//div[contains(@class, "page-layout_page_index")]'
one_categori_xpath = '//div[contains(@class, "page-layout_page_index")]//a'
search_string_img_xpath = '//span[contains(@class, "input_voice-search_yes")]'
one_image_in_search_xpath = '//div[contains(@class, "serp-item__preview")]/a'
opened_image_xpath = '//img[@class= "MMImage-Origin"]'
button_next_img_xpath = '//div[contains(@class, "CircleButton_type_next")]'
button_prev_img_xpath = '//div[contains(@class, "CircleButton_type_prev")]'

def does_element_exists (xpath):
    try:
        browser.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def wait_for_elemento (xpath):
    try:
        WebDriverWait(browser, 15).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
    except NoSuchElementException:
        return False
    return True

def save_img (img_name, img_savedname):
    response = requests.get(img_name, stream=True)
    with open(img_savedname, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def hash_it(img):
    with open(img, 'rb') as f:
        hasher = hashlib.md5()
        hasher.update(f.read())
        return hasher.hexdigest()

#step 1
browser.maximize_window()
browser.get(link)

if does_element_exists(checkbot_xpath) is True:
    checkforbot = browser.find_element(By.XPATH, checkbot_xpath)
    checkforbot.click()

wait_for_elemento(search_string_xpath)
search_string = browser.find_element(By.XPATH, search_string_xpath)
search_string.click()
#step 2

assert does_element_exists(button_menu_xpath) is True, 'Кнопка меню не найдена'

#step 3
browser.find_element(By.XPATH, button_menu_xpath).click()
browser.find_element(By.XPATH, button_img_xpath).click()

#step 4
browser.switch_to.window(browser.window_handles[1])
current_ssylca = browser.current_url
assert current_ssylca == required_url, f'Неверная ссылка ({current_ssylca}). Должна быть {required_url}'

#step 5
element = browser.find_element(By.XPATH, one_categori_xpath)
text_of_elem = element.text
element.click()

wait_for_elemento(search_string_img_xpath)

#step 6
text_in_url = browser.current_url
text_in_imgsearch = unquote(text_in_url).split('text=')[1]

assert text_in_imgsearch == text_of_elem, f'Текст элемента ({text_of_elem}) не совпадает с текстом в строке поиска ({text_in_imgsearch})'

#step 7
wait_for_elemento(one_image_in_search_xpath)
browser.find_element(By.XPATH, one_image_in_search_xpath).click()
#step 8

wait_for_elemento(opened_image_xpath)

first_img = browser.find_element(By.XPATH, opened_image_xpath).get_attribute('src')

#step 9
browser.find_element(By.XPATH, button_next_img_xpath).click()
second_img = browser.find_element(By.XPATH, opened_image_xpath).get_attribute('src')

#step 10
save_img(first_img, 'f_im.png')
save_img(second_img, 's_im.png')
first_hashim = hash_it('f_im.png')
sec_hashim = hash_it('s_im.png')

assert (first_hashim == sec_hashim) is False, 'Первая и вторая картинки одинаковы'

#step 11
browser.find_element(By.XPATH, button_prev_img_xpath).click()

#step 12
third_img = browser.find_element(By.XPATH, opened_image_xpath).get_attribute('src')
save_img(third_img, 't_im.png')
thir_hashim = hash_it('t_im.png')

assert first_hashim == thir_hashim, 'Начальная картинка и картинка при нажатии "Back" не совпадают'

browser.quit()