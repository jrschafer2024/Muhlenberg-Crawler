#Name: Alyssa Rotondo and Jessica Schafer
#Date: 12/5/23
#Description: This program crawls the muhlenberg.edu website and stores the content of the 10000 pages it crawled in txt files, along with a count of how many relative, absolute and total links were crawled, and total pages crawled.
#The number of relative, absolute, and total links as well as the number of pages crawled and content of the html file for each page crawled is stored in a txt file.
import os
import requests
import re 
import time
from urllib.parse import urlparse, urljoin

#This method stores the relative and absolute links and uses regex to extract html content links
def getLinks(htmlContent, baseUrl):
    relativeLinks = set() #store all relative links in a set
    absoluteLinks = set() #store all absolute links in a set
    linkPattern = re.compile(r'href=["\'](.*?)["\']') #regex to extract links
    links = linkPattern.findall(htmlContent) #uses regex to find all links in html content

    for link in links:
        if link.startswith('/'):  #string method to find the relative link
            relativeLinks.add(baseUrl + link) #a relative link has been found
        elif link.startswith(('http://', 'https://')): #an absolute link has been found
            absoluteLinks.add(link) #add to the set
    return relativeLinks, absoluteLinks
#This method confirms that crawling of a page is allowed in robots.txt; if not, the page will not be crawled
def crawlingAllowed(url):
    robotsUrl = urljoin(url, "/robots.txt")
    try:
        response = requests.get(robotsUrl)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {robotsUrl}: {e}") #if this happens, crawling is allowed
        return True  #crawling is allowed if there's an issue fetching robots.txt
    #check if crawling is allowed in robots.txt
    return "User-agent:" not in response.text or "Disallow: /" not in response.text #text inside of robots.txt

#This method retrieves the contents of a url from the html content 
def crawlPage(url, outputFolder, counter):
    try:
        response = requests.get(url) #retrieves contents of a url
        response.raise_for_status() #checks status code for request to fetch content; help from: https://www.youtube.com/watch?v=ULv9x0GQFbw
    except requests.exceptions.RequestException as error: #exceptions of requests; help from: https://www.youtube.com/watch?v=ULv9x0GQFbw
        print(f"Error fetching {url}: {error}") #help from: https://www.youtube.com/watch?v=ULv9x0GQFbw
        return 0, 0  #return 0 if there's an error
    time.sleep(1)
    htmlContent = response.text #fetches html content 
    baseUrl = response.url #fetches base url
    if not crawlingAllowed(baseUrl):
        print(f"Crawling not allowed for {baseUrl}")
        return 0, 0
    relativeLinks, absoluteLinks = getLinks(htmlContent, baseUrl) #used to extract relative and absolute links from the html
    #count the number of relative and absolute links:
    numRelativelinks = len(relativeLinks)
    numAbsolutelinks = len(absoluteLinks)
    #clean the text by replacing invalid characters in the URL for the filename:
    cleanUrl = re.sub(r'[^a-zA-Z0-9+]', '_', url) #regex shown in class demo
    filename = os.path.join(outputFolder, f"doc{counter}.txt")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, 'w', encoding='utf-8') as file: #writing all of this info to a txt file
            file.write(f"Url: {url}\n")
            file.write(f"Number of Relative Links: {numRelativelinks}\n")
            file.write(f"Number of Absolute Links: {numAbsolutelinks}\n")
            file.write(htmlContent)
    except IOError as e:
        print(f"Error writing file {filename}: {e}")
        return 0, 0

    return numRelativelinks, numAbsolutelinks

#This method actualy crawls the muhlenberg.edu website; it uses BFS to crawl the pages until it reaches 100
def crawlSite(startUrl, outputFolder, maxPages=8000): #actually crawling the website (I tested up to 8000 but the program will continue to 10000 pages)
    crawledPages = 0
    totalRelativelinks = 0
    totalAbsolutelinks = 0
    counter=1
    if not os.path.exists(outputFolder): #if it does not exist, create it
        os.makedirs(outputFolder)

    queue = [startUrl] #used for BFS approach--queue stores urls that have yet to be visited
    visited = set() #visited urls

    while queue and crawledPages < maxPages: #uses BFS to crawl the pages until it crawls 100 pages or the queue is empty
        currentUrl = queue.pop(0) #remove element from front of queue

        if currentUrl not in visited:
            visited.add(currentUrl) #add it to visited so the same url is not visited twice
            if crawlingAllowed(currentUrl):
                numRelativelinks, numAbsolutelinks = crawlPage(currentUrl, outputFolder, counter)
                totalRelativelinks += numRelativelinks #updates number of relative links for each url in the queue
                totalAbsolutelinks += numAbsolutelinks
                crawledPages += 1 #used for the count in the txt files
                counter+=1

                try: #try statements with exceptions below to avoid running the program then one url crashing it (as discussed in lecture)
                    response = requests.get(currentUrl) #fetches html content of page
                    links = re.findall(r'href=["\'](.*?)["\']', response.text) #regex to extract additional links
                    for link in links:
                        if link not in visited and link.startswith(('http://', 'https://')):
                            queue.append(link) #adds these links to the queue if they have not been seen already and are valid links
                except requests.exceptions.RequestException as error: #exceptions of requests; help from: https://www.youtube.com/watch?v=ULv9x0GQFbw
                    print(f"Error fetching links from {currentUrl}: {error}")

    print(f"\nCrawling finished. Retrieved {crawledPages} pages.")
    print(f"Total Relative Links: {totalRelativelinks}")
    print(f"Total Absolute Links: {totalAbsolutelinks}")
    print(f"Total Urls: {totalAbsolutelinks+totalRelativelinks}")


if __name__ == "__main__":
    startUrl = "https://muhlenberg.edu"  
    outputFolder = "output_files" 

    crawlSite(startUrl, outputFolder, maxPages=8000) #LOWER THE VALUE OF MAX PAGES FOR A FASTER RUNTIME
