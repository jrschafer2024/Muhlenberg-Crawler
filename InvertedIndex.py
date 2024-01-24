#Author: Jessica Schafer and Alyssa Rotondo
#Date: 5 December 2023
#Description: This program builds an inverted index using the files written while crawling the muhlenberg.edu website and allows the user to search 
#             for relevant documents with a GUI

#Importing necessary libraries
import os
import nltk
import requests
import re
import math
import tkinter as tk
import PIL

import threading
from tkinter import *
from PIL import Image, ImageTk

import webbrowser
import time

from nltk.stem import PorterStemmer
nltk.download("punkt")
ps = PorterStemmer()
from nltk.corpus import stopwords
 
nltk.download('stopwords')
nltk.download("wordnet")
nltk.download("omw-1.4")

#GUI CLASS
class MyGUI:
    #GUI CONSTRUCTOR: WINDOWS AND WIDGETS
    def __init__(self):

        #building the main GUI window
        self.root = tk.Tk()
        self.root.geometry("1000x600")
        self.root['bg'] = "salmon"
        self.root.title("Crawling through 'Berg")

        #building a grid for the search bar. 
        self.searchFrame = tk.Frame(self.root)
        self.searchFrame.columnconfigure(0,weight=1)
        self.searchFrame['bg'] = "spring green"

        #building the text box where the user will enter their query
        self.query = tk.Text(self.searchFrame,height=1,font=('Arial',16))
        self.query.grid(row=0,column=0)

        #building the button the user will press to search with their query
        self.search = tk.Button(self.searchFrame,text="Search",font=('Arial',16),command=self.run)
        self.search.grid(row=0,column=1,padx=10)

        #binding the frame with the search bar to the main window
        self.searchFrame.pack(padx=10,pady=10)

        #building a frame for the stopwords and stemming checkboxes
        self.booFrame = tk.Frame(self.root)
        self.booFrame.columnconfigure(0,weight=1)
        self.booFrame['bg'] = "spring green"

        self.stopwords = bool #variable to hold if the user wants to remove stopwords

        #building a checkbox the user can use to indicate if they want to remove stopwords
        self.stopCheck = tk.Checkbutton(self.booFrame, variable=self.stopwords, text="Remove Stopwords", onvalue=True, offvalue=False)
        self.stopCheck['bg'] = "spring green"
        self.stopCheck.grid(row=0,column=0, padx=10)

        self.stem = bool #variable to hold if the user wants to use stemming

        #building a checkbox the user can use to indicate if they want to use stemming
        self.stemCheck = tk.Checkbutton(self.booFrame, variable=self.stem, text="Use Stemming", onvalue=True, offvalue=False)
        self.stemCheck['bg'] = "spring green"
        self.stemCheck.grid(row=0,column=1, padx=10)

        #binding the frame with the checkboxes to the main window
        self.booFrame.pack(padx=10,pady=10)

        self.similarities = list() #list to hold the top ten most relative urls (returned from main())

        self.root.mainloop() #keep the program running until the user kills it. 

    #METHOD CALLED BY SEARCH BUTTON 
    def run(self):
        #This method uses multithreading to run the animation while the main function runs in the background
        #Help from: https://www.youtube.com/watch?v=A9mxZGV_zmI
        t = threading.Thread(target=self.getURLs) #attach the main function to a separate thread
        t.start() #start the function
        self.load() #on the main thread, run the animation 

    #METHOD TO RUN THE MAIN SEARCH FUNCTION AND STORE THE RETURNED LIST OF URLS
    def getURLs(self):
        self.similarities = main(self.query.get('1.0',"end-1c"), self.stem, self.stopwords) #searching with the query

        #building a frame on which the urls will be displayed
        self.resultGrid = tk.Frame(self.root)
        self.resultGrid.columnconfigure(3,weight=1)
        self.resultGrid['bg'] = "salmon"

        #MAKING THE STRINGS FUNCTIONAL HYPERLINKS
        #For each url in the returned list:
        link1 = tk.Label(self.resultGrid, text=self.similarities[0],font=('Arial',16),anchor="w", justify="left") #make a label for the string
        link1['bg'] = "spring green"
        link1.grid(row=0,column=0) #place the label in the frame
        link1.bind("<Button-1>", lambda e: self.openURL(self.similarities[0]) ) #bind the label to a button that, when pressed, opens the url
        #repeat for the next 9 links

        link2 = tk.Label(self.resultGrid, text=self.similarities[1],font=('Arial',16),anchor="w", justify="left")
        link2['bg'] = "spring green"
        link2.grid(row=1,column=0, pady=5)
        link2.bind("<Button-1>", lambda e: self.openURL(self.similarities[1]) )
        link3 = tk.Label(self.resultGrid, text=self.similarities[2],font=('Arial',16),anchor="w", justify="left")
        link3['bg'] = "spring green"
        link3.grid(row=2,column=0, pady=5)
        link3.bind("<Button-1>", lambda e: self.openURL(self.similarities[2]) )
        link4 = tk.Label(self.resultGrid, text=self.similarities[3],font=('Arial',16),anchor="w", justify="left")
        link4['bg'] = "spring green"
        link4.grid(row=3,column=0, pady=5)
        link4.bind("<Button-1>", lambda e: self.openURL(self.similarities[3]))
        link5 = tk.Label(self.resultGrid, text=self.similarities[4],font=('Arial',16),anchor="w", justify="left")
        link5['bg'] = "spring green"
        link5.grid(row=4,column=0, pady=5)
        link5.bind("<Button-1>", lambda e: self.openURL(self.similarities[4]) )
        link6 = tk.Label(self.resultGrid, text=self.similarities[5],font=('Arial',16),anchor="w", justify="left")
        link6['bg'] = "spring green"
        link6.grid(row=5,column=0, pady=5)
        link6.bind("<Button-1>", lambda e: self.openURL(self.similarities[5]) )
        link7 = tk.Label(self.resultGrid, text=self.similarities[6],font=('Arial',16),anchor="w", justify="left")
        link7['bg'] = "spring green"
        link7.grid(row=6,column=0, pady=5)
        link7.bind("<Button-1>", lambda e: self.openURL(self.similarities[6]) )
        link8 = tk.Label(self.resultGrid, text=self.similarities[7],font=('Arial',16),anchor="w", justify="left")
        link8['bg'] = "spring green"
        link8.grid(row=7,column=0, pady=5)
        link8.bind("<Button-1>", lambda e: self.openURL(self.similarities[7]) )
        link9 = tk.Label(self.resultGrid, text=self.similarities[8],font=('Arial',16),anchor="w", justify="left")
        link9['bg'] = "spring green"
        link9.grid(row=8,column=0, pady=5)
        link9.bind("<Button-1>", lambda e: self.openURL(self.similarities[8]) )
        link10 = tk.Label(self.resultGrid, text=self.similarities[9],font=('Arial',16),anchor="w", justify="left")
        link10['bg'] = "spring green"
        link10.grid(row=9,column=0, pady=5)
        link10.bind("<Button-1>", lambda e: self.openURL(self.similarities[9]) )

        #Help found: https://www.tutorialspoint.com/how-to-create-a-hyperlink-with-a-label-in-tkinter

        #building button to clear search results
        self.clear = tk.Button(self.resultGrid,text="Clear Results",font=('Arial',16),command=self.resultGrid.destroy)
        self.clear['bg'] = "spring green"
        self.clear.grid(row=10,column=0)
        self.similarities.clear() #clear list of urls so animation will run again if another query is entered

        self.resultGrid.pack(padx=10,pady=10) #binding the frame of urls to the main window
    
    #METHOD TO OPEN THE URLS
    def openURL(self, url):
        #Help found: https://www.tutorialspoint.com/how-to-create-a-hyperlink-with-a-label-in-tkinter
        webbrowser.open_new_tab(url)
   
   #METHOD TO RUN THE "LOADING" ANIMATION
    def load(self):
        #building a canvas on which the images will be placed and move
        self.canvas = Canvas(self.root,width=200,height=200)
        self.canvas['bg'] = "salmon"
        self.canvas['highlightthickness'] = 0
        self.canvas.pack(padx=200,pady=100)

        #setting the speed of movement
        xvelocity = 1 
        yvelocity = 1

        #initializing lists to hold the frames of each bug
        up = []
        down = []
        left = []
        right = []

        #Opening and storing each image
        up1= (Image.open("up1.png"))
        up2= (Image.open("up2.png"))
        down1= (Image.open("down1.png"))
        down2= (Image.open("down2.png"))
        left1= (Image.open("left1.png"))
        left2= (Image.open("left2.png"))
        right1= (Image.open("right1.png"))
        right2= (Image.open("right2.png"))

        #resizing each image so they are smaller 
        up1 = up1.resize((30,30), PIL.Image.LANCZOS)
        up2 = up2.resize((30,30), PIL.Image.LANCZOS)
        down1 = down1.resize((30,30), PIL.Image.LANCZOS)
        down2 = down2.resize((30,30), PIL.Image.LANCZOS)
        left1 = left1.resize((30,30), PIL.Image.LANCZOS)
        left2 = left2.resize((30,30), PIL.Image.LANCZOS)
        right1 = right1.resize((30,30), PIL.Image.LANCZOS)
        right2 = right2.resize((30,30), PIL.Image.LANCZOS)

        #FOR EACH PAIR OF IMAGES FOR THE LADYBUG FACING A CERTAIN DIRECTION:
        #make an image object from the resized image
        up1 = ImageTk.PhotoImage(up1)
        up2 = ImageTk.PhotoImage(up2)
        #append both images to the list of frames
        up.append(up1)
        up.append(up2)

        down1 = ImageTk.PhotoImage(down1)
        down2 = ImageTk.PhotoImage(down2)
        down.append(down1)
        down.append(down2)

        left1 = ImageTk.PhotoImage(left1)
        left2 = ImageTk.PhotoImage(left2)
        left.append(left1)
        left.append(left2)

        right1 = ImageTk.PhotoImage(right1)
        right2 = ImageTk.PhotoImage(right2)
        right.append(right1)
        right.append(right2)

        #placing the images at their starting positions
        u = self.canvas.create_image(150,15,image=up[0])
        d = self.canvas.create_image(15,150,image=down[0])
        l = self.canvas.create_image(15,15,image=left[0])
        r = self.canvas.create_image(150,150,image=right[0])

        count = 1 #variable to help switch between frames
        while len(self.similarities)==0: #while the main funtion has not finished running:
            #get the coordinates of each ladybug image
            ucoord = self.canvas.coords(u)
            dcoord = self.canvas.coords(d)
            lcoord = self.canvas.coords(l)
            rcoord = self.canvas.coords(r)

            #FOR THE LADYBUG IN EACH DIRECTION:
            if ucoord[0]==15: # if the ladybug has reached the end of the frame (end of it's walking path): 
                u = self.canvas.create_image(150,15,image=up[count%2]) #place the next frame at the beginning of it's path 
            else: #if the ladybug has not reach the end of its path:
                u = self.canvas.create_image(ucoord[0],ucoord[1],image=up[count%2]) #place the next frame at the spot of the current frame
                self.canvas.move(u,-xvelocity,0) #move the frame in the appropriate direction
            #repeat for the other three directions

            if dcoord[0]==150:
                d = self.canvas.create_image(15,150,image=down[count%2])
            else:
                d = self.canvas.create_image(dcoord[0],dcoord[1],image=down[count%2])
                self.canvas.move(d,xvelocity,0)
            if lcoord[1]==150:
                l = self.canvas.create_image(15,15,image=left[count%2])
            else:
                l = self.canvas.create_image(lcoord[0],lcoord[1],image=left[count%2])
                self.canvas.move(l,0,yvelocity)
            if rcoord[1]==15:
                r = self.canvas.create_image(150,150,image=right[count%2])
            else:
                r = self.canvas.create_image(rcoord[0],rcoord[1],image=right[count%2])
                self.canvas.move(r,0,-yvelocity)

            self.root.update() #update the main window with the newly positioned images
            count+=1 #increment count
            time.sleep(0.1)

        #When the main function has finished running: 
        self.canvas.destroy() #destroy the frame containing the images. 

        #Help from: https://www.youtube.com/watch?v=dF0OtdYVi_c
        #Help from: https://mail.python.org/pipermail/tkinter-discuss/2009-December/002138.html

#END OF GUI CODE

#BEGIN INVERTED INDEX CODE

#CLASS TO BUILD INVERTED INDEX
class InvertedIndexer:
    #CONSTRUCTOR METHOD - LOADS IN FILES WRITTEN WITH CRAWLER
    def __init__(self,folder):
        self.files = [] #list to hold all files in the directory
        dir_path = './'+folder+'/' #getting the direct path of the directory based on the parameter (spam or ham)

        #https://towardsthecloud.com/get-relative-path-python#:~:text=A%20relative%20path%20starts%20with,path%20to%20the%20file%20want.
        #https://www.boardinfinity.com/blog/python-list-files-in-a-directory/
        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file, if it is, add it to the list
            if os.path.isfile(os.path.join(dir_path, path)):
                self.files.append(path)

    #METHOD TO READ EACH FILE AND BUILD THE INVERTED INDEX
    def buildInvertedIndex(self, files, cwd, folder, stopword, stem):
        urls = dict() #dictionary to hold the filename(key) and the url(value)
        stop_words = set(stopwords.words('english')) #used to remove stop words
                                                     # credit to: https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
        os.chdir(cwd) #changing the directory to the directory of the file running the program
        dir_path = './'+folder+'/' #setting the cwd to the directory of the files
        os.chdir(dir_path)

        self.invertedIndex = dict() #dictionary that will be the inverted index
        self.maxFreq = dict() #dictionary to hold the max frequency of each file

        for filename in files: #for each file in this directory:
            file = open(filename,encoding='utf8',errors="ignore") #open and read
            lines = file.readlines() 

            #isolating the url (written at the top fo the file as "URL: *url*")
            url = lines[0] 
            url = url.split(" ")
            url = url[1]
            url = url.split("\n")
            url = url[0]

            urls[filename] = url #add url to the dictionary of filename:url
            page = requests.get(url) #access the url's html page
            htmlContent = page.text #get content of the url's html page
            
            #regex to clean html file
            #Help from: #https://medium.com/@jorlugaqui/how-to-strip-html-tags-from-a-string-in-python-7cb81a2bbf44
            clean = re.compile('<.*?>') #compile a pattern that searches for tags in the html
            htmlContent = re.sub(clean, '',htmlContent) #sub each tag with a blank space
            words = re.findall("[a-zA-Z0-9'-]+",htmlContent) #build list of all words in cleaned html content
            words = [word.lower() for word in words] #make each word completely lowercase

            for word in words: #for each word in the list of words:
                if stem: #if the user opted to use stemming:
                    word = ps.stem(word) #stem the word
                if stopword and word in stop_words: #if the user opted to remove a stopword and the word is a stopword:
                    continue #continue to the next word
                if word in self.invertedIndex.keys(): #if the word is already in the inverted index:
                    if filename not in self.invertedIndex[word].keys(): #if the file is not in the word's dictionary:
                        self.invertedIndex[word][filename]=1 #add the file to the word's dictionary with a value of 1
                        if(filename not in self.maxFreq.keys()): #if the file has not been added to the max frequencies dictionary:
                            self.maxFreq[filename] = 1 #intilialize the key with value 1
                    else: #if the file is in the word's dictionary: 
                        self.invertedIndex[word][filename]+=1 #increment the file's value
                        if self.invertedIndex[word][filename] > self.maxFreq[filename]: #if this new value is greater than the max frequency of the file:
                            self.maxFreq[filename] = self.invertedIndex[word][filename] #update the file's max frequency
                else: #if the word is not in the inverted index
                    self.invertedIndex[word] = dict() #build a dictionary for the word 
                    self.invertedIndex[word][filename]=1 #set the word frequency in the file to 1
                    if(filename not in self.maxFreq.keys()): #if the file has not been added to the max frequencies dictionary:
                            self.maxFreq[filename] = 1 #intilialize the key with value 1 
        
        return urls #return the dictionary of filename: url

#METHOD TO CALCULATE TFIDF OF THE QUERY
def queryRetrieval(stopword, stem, invertedIndex, maxFreq, query):
    stop_words = set(stopwords.words('english'))
    queryWords = query.split(" ") # getting a list of words in the query

    words = dict() #dictionary to act as inverted index for query
    Qtfidf = dict()
    maxFreqQ = 0 #variable to hold the max frequency of the query
    denomQ = 0 #variable to calculate the vector length of the query

    for word in queryWords: #for each word in the query:
        if stem: #if the user opted to use stemming:
            word = ps.stem(word) #stem the word
        if stopword and word in stop_words: #if the user opted to remove stopwords and the word is a stopword:
            continue #continue to the next word
        if word in words.keys(): #if the word is in the query's inverted index:
            words[word]+=1 #increment the value
            if words[word]>maxFreqQ: #if the frequency of the word is greater than the max frequency o the query:
                maxFreqQ = words[word] #update the max frequency
        else: #if the word is not in the query's inverted index:
            words[word]=1 #add it to the dictionary with vallue 1
            if words[word]>maxFreqQ: #if the frequency of the word is greater than the max frequency o the query:
                maxFreqQ = words[word] #update the max frequency
        
    for word in words.keys(): #for each word in the query's inverted index:
        tf = words[word]/maxFreqQ #tf = the frequency of the word/the max frequency of the query
        if word in invertedIndex: #if the word is in the inverted index:
            #idf = log(number of files (+query) / the number of files (+query) in which the word appears) 
            idf = math.log((len(maxFreq.keys())+1)/(len(invertedIndex[word].keys())+1),10)
        else: #if the word is not in the inverted index (meaning it's only in the query):
            #idf = log(number of files (+query) / 1)
            idf = math.log((len(maxFreq.keys())+1)/(1),10)
        idf+=1 #smooth idf so it cannot be zero
        Qtfidf[word] = tf*idf #calculate tfidf and store it as the value of the word in the dictionary
        denomQ+=(tf*idf)**2 #add tfidf squared to the denominator variable

    denomQ = math.sqrt(denomQ) #take the square root of the denominator
    #denomQ  now equals the vector length of the query

    return Qtfidf, denomQ

#METHOD TO CALCULATE TFIDF FOR EACH WORD IN THE QUERY FOR A FILE        
def documentRetrieval(stopword, stem, invertedIndex, maxFreq, query, filename, Qtfidf, denomQ):
    stop_words = set(stopwords.words('english'))
    queryWords = query.split(" ") #getting the list of words in the query

    words = [] #list to hold the words after preprocessing
    num = 0 #variable to calculate the sum of the products of the tfidf of the word in the query and the file
    denom = 0 #variable to calculate the vector length of the file

    for word in queryWords: #for each word in the query:
        if stem: #if the user opted to use stemming:
            word = ps.stem(word) #stem the word
        if stopword and word in stop_words: #if the user opted to remove stopwords and the word is a stopword:
            continue #move to the next word
        if word not in words: #if the word has not already been added:
            words.append(word) #add the word to the list of words

    for word in words: #for each word:
        if word in invertedIndex.keys() and filename in invertedIndex[word].keys(): #if the word is in the inverted index and the file:
            tf = invertedIndex[word][filename]/maxFreq[filename] #tf = the frequency of the term in the file / the max frequency of the file
             #idf = log(number of files (+query) / the number of files (+query) in which the word appears)
            idf = math.log((len(maxFreq.keys())+1)/(len(invertedIndex[word].keys())+1),10)
            idf+=1 #smooth idf so it cannot be zero
            num+=((tf*idf)*Qtfidf[word]) #add the product of tfidf and the tfidf of the word in the query to the numerator
            denom+=(tf*idf)**2 #square the tfidf and add it to the denominator

    denom = math.sqrt(denom) #take the square root of the denominator 
    #denomQ  now equals the vector length of the file using the words in the query

    if denom > 0: #if any of the words appeared in the file:
        cosine = num/(denom*denomQ) #calculate the cosine similarity
    else: #if none of the words appeared in the file:
        cosine = 0 #the cosine is 0

    return cosine #return the cosine similarity
    
#METHOD TO COMPARE THE COSINE SIMILARITIES OF EACH FILE
def main(entry, stem, stopword):

    urls = dict() #dictionary of filenames and urls

    cwd = os.getcwd() #get the current working directory
    II = InvertedIndexer("output_files") #initialize instance of the Inverted Index class
    urls = II.buildInvertedIndex(II.files,cwd,"output_files",stopword,stem) #build the inverted index

    os.chdir(cwd) #return to the directory of this program

    query=entry.lower() #convert each word in the query to lowercase
    Qtfidf, denomQ = queryRetrieval(stopword,stem,II.invertedIndex,II.maxFreq,query) #call function to get tdidf of each word in the query

    cosineSimilarities = dict() #dictionary to hold the cosine similarities of each file

    for filename in II.files: #for each file:
        #get the cosine similarity and store it in the dictionary
        cosineSimilarities[filename] = documentRetrieval(stopword,stem,II.invertedIndex,II.maxFreq,query,filename,Qtfidf,denomQ)

    #sort the dictionary of cosine similarities in descending order
    #Help from: https://sparkbyexamples.com/python/how-to-sort-dictionary-by-value-in-python/
    sorted_list = sorted(cosineSimilarities.items(), key = lambda x:x[1], reverse=True) 
    cosineSimilarities.clear()
    for key, value in sorted_list:
        if len(cosineSimilarities.keys())<10:
            cosineSimilarities[key] = value
        else:
            break

    sortedURLs = list() #list of the top ten urls

    for key in cosineSimilarities.keys():
        sortedURLs.append(urls[key]) #append url (not filename)
    print("done")
    return sortedURLs #return the list of urls

if __name__ == "__main__":
    MyGUI()