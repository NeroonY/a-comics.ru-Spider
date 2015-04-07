
# -*- coding: UTF-8 -*-
#Batch downloading web-comics from www.a-comics.ru.

import urllib
import os
import leaf
import logging

# logging.basicConfig(level = logging.DEBUG)

buffer_file_name = './data/comic_page.htm'
result_file_name = 'results.txt'
save_folder = "./Saved"

# buffering = True #for debug only
buffering = False
skip_doubles = True #skip already downloaded

def GetDomain(url):
	parts = url.split('//', 1)
	return parts[0]+'//'+parts[1].split('/', 1)[0]

def LoadPage(page_url):
	if buffering and os.path.exists(buffer_file_name):
		logging.info( u'Used saved page')

		page = open(buffer_file_name).read()
		page = page.decode('utf8')
	else:
		logging.info( u'Load web-page')

		page = urllib.urlopen(page_url).read()
		if buffering:
			buf_file = open(buffer_file_name, 'w')
			buf_file.write(page)
			buf_file.close()
	return page	
	

def SaveImage(img_url, destination):
	logging.info( 'load' + img_url)

	
	urllib.urlretrieve(img_url, destination)

#return local path
def GetImageUrl(page):
	doc = leaf.parse(page)
	data = doc('.issue img')
	logging.info(data)

	logging.info( 'Found img links' + str(len(data)))
	

	if len(data) == 1 :
		img_block = data[0]
		if hasattr(img_block, 'src'): 
			logging.info(data[0].src )
			return data[0].src

def ProcessPage(page_url, img_dist_name):
	if skip_doubles and os.path.exists(img_dist_name):
		return

	logging.info( 'Load ' + page_url)
	page = LoadPage(page_url)
	img_url = GetDomain(page_url) + GetImageUrl(page)
	SaveImage(img_url,img_dist_name)

def PrepareSavePlace(folder_name):
	if not os.path.exists(folder_name):
		os.makedirs(folder_name)

#images save to folder %comic_name%,auto extracting from url
def ProcessComicSubSite(page_url):
	url_parts = page_url.rsplit('/',2)
	main_url = url_parts[0] + '/' + url_parts[1]
	comic_name = url_parts[1]
	last_index = int(url_parts[2])

	full_save_folder = os.path.join(save_folder, comic_name)
	PrepareSavePlace(full_save_folder)
	#доп нули для единобразия и правильной сортировки
	img_name_mask = '%0' + str(len(str(last_index))) + 'd.jpg'


	for i in xrange(1, last_index + 1):
		ProcessPage(main_url + '/' + str(i), os.path.join(full_save_folder, img_name_mask % i))

#ProcessPage('http://acomics.ru/~arthas/3', 't.png')
#ProcessComicSubSite('http://acomics.ru/~arthas/10')
