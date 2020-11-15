# -*- coding: utf-8 -*-
"""
Web Crawler

Created on Tue Nov 12 17:03:03 2019

@author: Alex
"""
import time
import requests
import re


def main():
    global stack
    global currenturl
    global filenumber
    global calls
    global visitedurls
    visitedurls = []
    calls = 0
    filenumber = 0
    currenturl = 'https://www.muhlenberg.edu/'
    stack = []
    getRobots('https://www.muhlenberg.edu/robots.txt')
    getHomepage(currenturl, calls)
    
def getRobots(URL):
    
    robots = requests.get(URL)
    f = open("robots.txt", "wb")

    f.write(robots.content)

def getHomepage(currenturl, calls):
    
    r = requests.get(currenturl)
    
    f = open("links.txt", "wb")
    f.write(r.content)
    cleanLinks(filenumber, calls)

def getPage(currenturl, filenumber, calls):
    print(currenturl)
    r = requests.get(currenturl)    
    f = open("links.txt", "wb")
    f.write(r.content)
    cleanLinks(filenumber, calls)
    
    
def cleanLinks(filenumber, calls):
    abscount = 0
    relcount = 0
    filename = "Sample" + str(filenumber) + ".txt"
    print(filename)
    file = open("links.txt", "r")
    filecontents = file.readlines()
    filecontents = str(filecontents)
    
    robots = open("robots.txt", "r")
    robotstxt = robots.readlines()
    weblinks = re.compile(r'<a[^<>]+?href=([\'\"])(.*?)\1')  
    file2 = open(filename, "w")


    links = re.findall(weblinks, filecontents)
    for i in links:
        for j in robotstxt:
            if j != i:
                if i[1][0] == "/" and len(i[1]) != 1:  
                    relcount+=1
                    fixedlink = "https://www.muhlenberg.edu" + i[1]
                    stack.append(fixedlink)
                    file2.write(fixedlink)
                    file2.write("\n")
                
                if i[1][0] == "h":
                    abscount+=1
                    stack.append(i[1])
                    file2.write(i[1])
                    file2.write("\n")
                        
    absolute = "absolute:" + str(abscount)
    relative = "relative:" + str(relcount) 
    current = "current url:" + currenturl            
    file2.write(current)
    file2.write("\n")
    file2.write(absolute)
    file2.write("\n")
    file2.write(relative)
    fileName(filenumber, calls, currenturl)
    
def fileName(filenumber, calls, currenturl):
    filenumber+=1
    print(filenumber)
    visitedurls.append(currenturl)
    sameurl = 0
    while sameurl == 0:
        if currenturl in visitedurls:
            currenturl = stack.pop()
        else:
            sameurl = 1
    visitedurls.append(currenturl)  
    time.sleep(1)    
    calls = calls+1
    if calls <= 3:
        getPage(currenturl, filenumber, calls)

if __name__ == "__main__":
    main()