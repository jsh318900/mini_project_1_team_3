import requests
import selenium
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from time import sleep

def yearchart(year):
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
    driver = webdriver.Chrome()
    driver.get('https://www.melon.com/index.htm')

    driver.implicitly_wait(10)

    
    elem = driver.find_element_by_class_name('menu_bg.menu01')
    elem.click()  #멜론차트 클릭 


    elem = driver.find_element_by_css_selector('#gnb_menu > ul:nth-child(1) > li.nth1.on > div > div > button')
    elem.click()   
#차트파인더 클릭 #gnb_menu > ul:nth-child(1) > li.nth1.on > div > div > button

    elem = driver.find_element_by_css_selector('#d_chart_search>div>h4.tab03>a')
    elem.click()
#연도차트 클릭

#연대선택-2000년대
    decade_to_element_id = {2000:'decade_3', 2010:'decade_2'}
    decade = 0 
    if 2000 <= year <= 2009:
        decade = 2000
    elif 2010 <= year <=2019:
        decade = 2010
    decade_button = driver.find_element_by_id(decade_to_element_id[decade])
    decade_button = decade_button.find_element_by_xpath('..') #부모 엘리먼트
    decade_button.click()
    
    #연도선택-
    i = (decade + 10) - year 
    decade_button = driver.find_element_by_id('year_{}'.format(i))
    decade_button = decade_button.find_element_by_xpath('..') #부모 엘리먼트
    decade_button.click()

#장르선택 - 국내종합 선택
 
    if year <= 2004 :
        decade_button = driver.find_element_by_id('gnr_1')
        decade_button = decade_button.find_element_by_xpath('..') #부모 엘리먼트
        decade_button.click()
    else :
        decade_button = driver.find_element_by_id('gnr_2')
        decade_button = decade_button.find_element_by_xpath('..') #부모 엘리먼트
        decade_button.click()

    #검색 클릭
    elem = driver.find_element_by_css_selector('button.btn_b26')
    elem.click()
    
    
# 3. 필요한 정보 가져오기 위해 구문 분석
    sleep(3)
    soup = BeautifulSoup(driver.page_source, 'lxml')

#순위 
    ranks = soup.select('span.rank')
    ranks = [rank.text for rank in ranks[0:51]]
            
#노래제목id -> 50개
    songs = soup.select('#lst50 > td:nth-child(4) > div > a') 

    song_list=[]
    for song_id in songs:
        song_list.append(song_id['href']) 
     
    search = 'javascript:'
    song_list = [song.strip(search) for song in song_list] 
  


 #가수id -> 54개
    singers = soup.select('#lst50 > td:nth-child(4) > div > div > div:nth-child(3) > div.ellipsis.rank02 > a')
        
    singer_list=[]
    for singer_id in singers:
        singer_list.append(singer_id['href']) 
    
    singer_list = [singer.strip(search) for singer in singer_list] 
    

#앨범제목 id -> 50개
    albums = soup.select('#lst50 > td:nth-child(4) > div > div > div:nth-child(3) > div.ellipsis.rank03 > a')
    

    album_list=[]
    for album_id in albums:
        album_list.append(album_id['href'])
    
    search = 'javascript:'
    album_list = [album.strip(search) for album in album_list ] 
   
 #좋아요 수 
    likes = []
    likes = soup.select('span.cnt')
    likes = [int(like.text.split('\n')[-1].replace(',', '')) for like in likes[0:50]]

        
    #zip(rank, song_list, album_list, likes)

# 2. 페이지 스크롤
# Java Script의 스크롤 기능을 통해서 더 많은 이미지를 가져옴
    prev_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

        curr_height = driver.execute_script('return document.body.scrollHeight')
     
        if prev_height == curr_height:
            break
            prev_height = curr_height
     
            #51위~100위
    elem = driver.find_element_by_css_selector('#frm > div.paginate.chart_page > span > a')
    elem.click()
    
    ranks_2 = []
    ranks_2 = soup.select('div.wrap.right_none>span.rank')
    ranks_2 = [rank.text for rank in ranks_2[51:]]
            
#노래제목id -> 50개
    songs = soup.select('#lst50 > td:nth-child(4) > div > a') 

    for song_id in songs:
        song_list.append(song_id['href']) 
     
    search = 'javascript:'
    song_list = [song.strip(search) for song in song_list] 
  


 #가수id -> 54개
    singers = soup.select('#lst50 > td:nth-child(4) > div > div > div:nth-child(3) > div.ellipsis.rank02 > a')
        
    for singer_id in singers:
        singer_list.append(singer_id['href']) 
    
    singer_list = [singer.strip(search) for singer in singer_list] 
    

#앨범제목 id -> 50개
    albums = soup.select('#lst50 > td:nth-child(4) > div > div > div:nth-child(3) > div.ellipsis.rank03 > a')
    
    for album_id in albums:
        album_list.append(album_id['href'])
    
    search = 'javascript:'
    album_list = [album.strip(search) for album in album_list ] 
   
 #좋아요 수 
    likes_2 = []
    likes_2 = soup.select('span.cnt')
    likes_2 = [int(like.text.split('\n')[-1].replace(',', '')) for like in likes_2[51:101]]
    
    ranks.extend(ranks_2)
    likes.extend(likes_2)

    return list(zip(ranks, song_list)), singer_list, album_list, likes