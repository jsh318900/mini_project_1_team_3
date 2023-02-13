import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time

decade_to_element_id = {}
for i in range(2):
    year = 2010 - i*10
    id = 'decade_{0}'.format(i+1)
    decade_to_element_id[year] = id
        
def ten_year(year):
    url = "https://www.melon.com/index.htm"

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get(url)

    elem = driver.find_element_by_css_selector('#gnb_menu > ul:nth-child(1) > li.nth1 > a > span.menu_bg.menu01')
    elem.click()

    elem = driver.find_element_by_css_selector('#gnb_menu > ul:nth-child(1) > li.nth1.on > div > div > button > span')
    elem.click()

    elem = driver.find_element_by_css_selector('#d_chart_search > div > h4.tab04 > a')
    elem.click()

    decade_button = driver.find_element_by_id(decade_to_element_id[year]) 
    decade_button = decade_button.find_element_by_xpath('..')
    decade_button.click()

    elem_id = 'gnr_1'
    button = driver.find_element_by_id(elem_id) 
    button = button.find_element_by_xpath('..')
    button.click()

    elem = driver.find_element_by_css_selector('#d_srch_form > div.wrap_btn_serch > button > span > span')
    elem.click()
    
    ranks = driver.find_elements_by_class_name("rank")
    lst_r1 = []
    for rank in ranks:
        lst_r1.append(rank.text)
        lst_r1 = [x for x in lst_r1 if x != '']
    driver.execute_script('movePage(2)')
    lst_r2 = []
    for rank in ranks:
        lst_r2.append(rank.text)
        lst_r2 = [x for x in lst_r2 if x != '']
    ranking = lst_r1 + lst_r2
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    lst_s = []
    info_s = soup.select("a.btn.btn_icon_detail")
    for info in info_s:
        link_s = info.attrs['href'][11:]
        lst_s.append(link_s)  
        
    lst_album = []
    info_albums = soup.select("div.ellipsis.rank03 > a")
    for info_album in info_albums:
        link_album = info_album.attrs['href'][11:]
        lst_album.append(link_album)
            
    lst_singer = []
    singers = soup.select("div.ellipsis.rank02 > a")
    for singer in singers:
        link_singer = singer.attrs['href'][11:]
        lst_singer.append(link_singer)

    total = list(zip(ranking, lst_s, lst_album))
    
    return total, lst_singer