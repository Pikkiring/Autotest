
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
browser = webdriver.Chrome(chrome_options)

link = "https://ya.ru/"
required_link = 'https://tensor.ru/'

##Xpaths:
checkbot_xpath = '//input[@class="CheckboxCaptcha-Button"]'
search_string_xpath = '//input[contains(@class ,"search3__input")]'
popup_suggest_xpath = '//ul[contains(@class, "mini-suggest__popup-content")]'
search_result_xpath = '//ul[@id = "search-result"]'
search_first_result_xpath = '//ul[@id = "search-result"]/li'
search_a_attribute_xpath = '//ul[@id = "search-result"]/li//a'
button_to_close_yawindow_xpath = '//span[contains(@class, "Icon_type_close24White")]'

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

#step 1
browser.maximize_window()
browser.get(link)

if does_element_exists(checkbot_xpath) is True:
    checkforbot = browser.find_element(By.XPATH, checkbot_xpath)
    checkforbot.click()

#step 2
wait_for_elemento(search_string_xpath)

#step 3
search_string = browser.find_element(By.XPATH, search_string_xpath)
search_string.send_keys("Тензор")

#step 4
assert does_element_exists(popup_suggest_xpath), "Таблица с подсказками не найдена"

#step 5
search_string.send_keys(Keys.ENTER)

wait_for_elemento(button_to_close_yawindow_xpath)
webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()

#step 6
assert does_element_exists(search_result_xpath) is True, 'Страница результатов поиска ни появилась'

#step 7
first_link_on_search = browser.find_element(By.XPATH, search_a_attribute_xpath)
href_attrib = first_link_on_search.get_attribute('href')

assert href_attrib == required_link, f'Первая ссылка не ведет на сайт {required_link}, а ведет на {href_attrib}'

browser.quit()