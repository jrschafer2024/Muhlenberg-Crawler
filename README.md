# Muhlenberg-Crawler
Built in collaboration with Alyssa Rotondo, the Muhlenberg Crawler crawls the muhlenberg.edu website and returns the top ten most relevent pages from the site based on a user-inputted query. 

To interact with this program, download each file and store them all in the same directory. 
1) Run the Python file titled "Crawler.py". This file will create a new folder titled "output_files" which is used by the second file.
   NOTE: This program is set to crawl and store 8,000 files from muhlenberg.edu. This causes a long runtime. For a faster runtime, change the value of "maxPages". This value is on the last line of code in 
   Crawler.py. It is a parameter in the "crawlSite" function call.
2) Run the Python file titled "InvertedIndex.py". This program includes a GUI using tkinter. 
