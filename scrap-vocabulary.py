#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Python3 script to scrape HTML text
"""

import urllib.request
from bs4 import BeautifulSoup
import sys
import codecs
import time


# delay in seconds to wait between each scraping
delay = 2

def get_soup(url):
    print("Parse url " + url)
    page = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
    soup = BeautifulSoup(page,'html.parser')
    soup.prettify()
    return soup

def getlisturls(url):
    soup = get_soup(url)
    
    ul = soup.find_all("ul")
    a_items = []
    for u in ul:
        aa = u.findAll("a")
        a_items.extend(aa)
    print ("Found " + str(len(a_items)) + " links")
    mylist=[]
    for a in a_items:
        mylist.append((a.text.strip(),a["href"].strip()))
    return mylist
    
def parse_article(url):
    soup = get_soup(url)
    return soup.find('article')

def skip(txt,ignore_list):
    for i in ignore_list:
        if txt.startswith(i):
            return True
    return False

def file2list(fname):
    """
      Convert all lines from given file into a list
    """
    with  codecs.open(fname,"r","utf-8") as file:
        return file.read().splitlines()

def tofile(f,txt):
    """
      write text to file with trailing line break 
    """
    f.write(txt + "\n")

# Process article url
def tohtml(url,name):
    print("Process " + name)
    a = parse_article(url)    
    h1 = a.find('h1')
    
    ignorelist = file2list("skip.txt")
    
    result = '<a name="' + name + '"></a>'
    result += '<h1>' + h1.text + '</h1>'
    ps = a.find_all("p")
    for p in ps:
        if skip(p.text,ignorelist):
            continue
        result += p.decode()
    return result

def createpage(baseurl,listurl,page_title,output_file):
    a_items = getlisturls(listurl)
    
    f = codecs.open(output_file,"w","utf-8")
    
    # generate html page
    tofile(f,'<!DOCTYPE html>')
    tofile(f,'<html>')
    tofile(f,'<head>')
    tofile(f,'<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">')
    tofile(f,'<style type="text/css">')
    tofile(f,'body { font-size: 20px;}')
    tofile(f,'</style>')
    tofile(f,'<title>'+page_title+'</title>')
    tofile(f,'</head>')
    tofile(f,'<body>')
    
    tofile(f,'<div class="content">')
    tofile(f,'<h1>' + page_title + '</h1>')
    tofile(f,'<ul class="index">')
    for a in a_items:
        tofile(f,'<li><a href="#'+a[0]+'">'+a[0]+'</a></li>')
    
    for a in a_items:
        tofile(f,tohtml(baseurl + "/" + a[1],a[0]))
        time.sleep(delay)
    tofile(f,'</ul>')
    tofile(f,'</div>')
    tofile(f,'</body></html>')
    
    f.close()
    
def main():
    baseurl = sys.argv[1]
    listurl = sys.argv[2]
    pagetitle = sys.argv[3]
    createpage(baseurl,listurl,pagetitle,"vocabulary.html")
    
if __name__ == "__main__":
    main()


