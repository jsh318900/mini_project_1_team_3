from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
MELON_URL = 'https://www.melon.com/index.htm'
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument('user-agent=' + USER_AGENT)
DRIVER_PATH = './webscraper/chromedriver'
DECADE_TO_ELEMENT_ID = {2000:'decade_3', 2010:'decade_2'}

def initialize_driver(driver_path = DRIVER_PATH, options=OPTIONS):
	driver = webdriver.Chrome(driver_path, options=options)
	driver.implicitly_wait(10)
	driver.get(MELON_URL)

	return driver

def navigate_to_year_chart(year):
	"""
	메인페이지에서 연도별차트까지 이동한 다음 해당 드라이버 리턴
	"""
	driver = initialize_driver()

	# 멜론차트 버튼 찾아서 클릭
	driver.find_element_by_css_selector('span.menu_bg.menu01').click()
	# 차트파인더 버튼 찾아서 클릭
	driver.find_element_by_css_selector('button.btn_chart_f').click()
	# 연도별 차트 버튼 찾아서 클릭
	driver.find_element_by_css_selector('h4.tab03>a').click()
	
	# 연대 선택
	decade = 2000 if 2000 <= year <= 2009 else 2010	
	driver.find_element_by_id(DECADE_TO_ELEMENT_ID[decade]).find_element_by_xpath('..').click()

	# 연도 선택
	year_id = 'year_{}'.format(range(10, 0, -1)[year - decade])
	driver.find_element_by_id(year_id).find_element_by_xpath('..').click()
	
	# 국내 종합 선택한 뒤 검색
	korea_id = 'gnr_2' if year >= 2005 else 'gnr_1'
	style_button = driver.find_element_by_id(korea_id).find_element_by_xpath('..')
	search_button = driver.find_element_by_css_selector('button.btn_b26')
	style_button.click()
	search_button.click()

	return driver

def scrap_song_page(song_id, driver=None):
	if driver is None:
		driver = initialize_driver()
	driver.execute_script('melon.link.goSongDetail("{}")'.format(song_id))
	artist_list = driver.find_element_by_css_selector('div.artist')
	artist_list = artist_list.find_elements_by_css_selector('a.artist_name')
	artist_list = [int(a.get_attribute('href').split("'")[1]) for a in artist_list]
	song_name = driver.find_element_by_class_name('song_name').text.strip()
	genre = driver.find_element_by_css_selector('div.meta>dl>dd:nth-child(6)').text.strip()
	num_like = int(driver.find_element_by_id('d_like_count').text.replace(',', ''))
	review_cnt = int(driver.find_element_by_id('revCnt').text.replace(',', '')[:-1])

	return {'id':song_id,
		    'name':song_name,
		    'singers':artist_list,
		    'genre':genre,
		    'num_like':num_like,
		    'num_comment':review_cnt}

def scrap_singer_page(singer_id, driver=None):
	if driver is None:
		driver = initialize_driver()
	driver.execute_script('melon.link.goArtistDetail({});'.format(singer_id))
	soup = BeautifulSoup(driver.page_source, 'lxml')
	name = soup.select_one('p.title_atist').text[5:]

	if '\xa0' in name:
		name = name.split('\xa0')[0]

	num_fan = int(soup.select_one('#d_like_count').text.replace(',', '')) 
	columns = soup.select('dt')
	debut_date, artist_type, company_name = None, None, None
	for c in columns:
		if c.text == '데뷔':
			debut = list(c.find_next_sibling().children)[1].text
			if '\n' in debut:
				debut_date = debut.split()[0]
			else:
				debut_date = debut
		elif c.text == '활동유형':
			artist_type = c.find_next_sibling().text
		elif c.text == '소속사':
			company_name = c.find_next_sibling().text

	return {'id':singer_id,
			'name':name,
			'artist_type':artist_type,
			'company':company_name,
			'debut_date':debut_date,
			'num_fan':num_fan}

def scrap_album_page(album_id, driver=None):
	if driver is None:
		driver = initialize_driver()
	driver.execute_script('melon.link.goAlbumDetail("{}")'.format(album_id))
	soup = BeautifulSoup(driver.page_source, 'lxml')
	name = soup.select_one('div.song_name').text.split('\n')[2].strip()
	artist_list = soup.select('div.artist>a.artist_name')
	artist_list = [x['href'].split("'")[1] for x in artist_list]
	release_date = soup.select_one('div.meta>dl>dd:nth-child(2)').text
	num_like = int(soup.select_one('#d_like_count').text.replace(',', ''))
	rating = float(soup.select_one('#gradPointLayer').text)
	num_rating = int(soup.select_one('#gradCountLayer').text.replace(',', '')[:-1])
	num_comment = int(soup.select_one('#revCnt').text.replace(',', '')[:-1])

	song_list = [a['href'] for a in soup.select('a.song_info')]
	song_list = [x.split("'")[1] for x in song_list]


	return {
		'id': album_id,
		'name':name,
		'release_date':release_date,
		'num_like':num_like,
		'rating':rating,
		'num_rating':num_rating,
		'num_comment':num_comment
	}, artist_list, song_list

