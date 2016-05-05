#!/usr/bin/env python2

import argparse
import json
import requests
import pypub
from bs4 import BeautifulSoup
import os
from colorama import Fore, init

SAFARI_USER=os.getenv("SAFARI_USER")
SAFARI_PASSWORD=os.getenv("SAFARI_PASSWORD")
HTML_STR =  "<html> <title> {} </title> <body> {} </body> <html>"
book = "https://www.safaribooksonline.com/library/view/fluent-python/9781491946237"
BOOK_ID = "9781491946237"

URL = "https://www.safaribooksonline.com"

API_ENDPOINT = URL + "/api/v1/book/"

headers = {
    'Origin': 'https://www.safaribooksonline.com',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8,hi;q=0.6',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.safaribooksonline.com/accounts/login/',
}


with requests.Session() as s:

	r = s.get(URL+'/accounts/login/')

	soup = BeautifulSoup(r.text, "lxml")
	csrftoken = soup.find_all("input")[0]['value']

	data = 'csrfmiddlewaretoken={}&email={}&password1={}&login=Sign+In&next='.format(
			csrftoken, SAFARI_USER,SAFARI_PASSWORD)

	r = s.post(URL+'/accounts/login/', headers=headers, data=data)
	r = s.get(API_ENDPOINT + BOOK_ID, headers=headers, data=data)
	
	j = json.loads(r.text)

	title = j['title']
	ebook = pypub.Epub(title)

	for index in j['chapters']:
		data = json.loads(s.get(index).text)
		web_url = data['web_url']
		chapter_title = data['title']
		html = BeautifulSoup(s.get(web_url).text, "lxml")
		try:
			chapter_html = html.find_all("section", class_="chapter")[0]
			chapter=pypub.create_chapter_from_string(HTML_STR.format(
						chapter_title, chapter_html), title=chapter_title)

			ebook.add_chapter(chapter)
		except Exception as e:
			print index, e
	ebook.create_epub("/home/ayush/", epub_name=title)
