#coding to search a list of books from the target source site
#works with Beautiful Soup 4

import urllib2
import re
from bs4 import BeautifulSoup
packtpub_url="http://www.packtpub.com"

#opens the url, according to page type
def get_booksurls(url): #create object
	page=urllib2.urlopen(url)
	soup_packtpage = BeautifulSoup(page, "lxml")
	page.close()
	next_page_li = soup_packtpage.find("li", class_="pager-nextlast")
	if next_page_li is None:
		next_page_url = None
		else
		next_page_url = packtpub_url + next_page_li.a.get('href')
	return next_page_url

	start_url = "www.packtpub.com/books"
	continue_scrapping = True
	books_url = [start_url]
	while continue_scrapping:
		next_page_url = get_booksurls(start_url)
		if next_page_url is None:
			continue_scrapping = False
		else:
			books_url.append(next_page_url)
			start_url = next_page_url

#holds the url t the detail page for each book
def get_bookdetails(url):
	page = urllib2.urlopen(url)
	soup_packtpage = BeautifulSoup(page, "lxml")
	page.close()
	all_books_table = soup_packtpage.find("table",class_="views-view-grid")
	all_book_titles =all_books_table.find_all("div",class_="views-field-title") 
	isbn_list = []
	for book_title in all_book_titles:
		book_title_span = book_title.span
		print("Title Name: " + book_title_span.a.string)
		print("URL: " + book_title_span.a.get("href"))
		price = book_title.find_next("div",class_="views-field-sell-price")
		print("PacktPub Price:" + price.span.string)    
		isbn_list.append(get_isbn(book_title_span.a.get('href')))  
	return isbn_list

#retrieve ISBN no. in comparison with each other
def get_isbn(url):
	book_title_url=packtpub_url + url
	page = urllib2.urlopen(book_title_url)
	soup_bookpage = BeautifulSoup(page, "lxml")
	page.close()
	isbn_tag = soup_bookpage.find('b', text = re.compile("ISBN:"))
	return isbn_tag.next_sibling
	isbns = []
	for bookurl in books_url:
		isbns += get_bookdetails(bookurl)

#retrieves selling price from a given website, in this example Amazon
def get_sellingprice_amazon(isbn):
	url_foramazon = "http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=" 
	url_for_isbn_inamazon = url_foramazon + isbn 
	page = urllib2.urlopen(url_for_isbn_inamazon)
	soup_amazon = BeautifulSoup(page, "lxml")
	page.close()
	selling_price_tag = soup_amazon.find('div', class_="newPrice")
	if selling_price_tag:
		print("Amazon Price" + selling_price_tag.span.string)

