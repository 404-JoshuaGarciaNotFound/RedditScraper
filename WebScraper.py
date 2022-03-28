from os import link
import requests
import re
import time
#import pandas as pd
from bs4 import BeautifulSoup

#MAKE SETUP. Min time for refresh
#ADD PM USER LINK
#ADD PRICE ESTIMATOR
#ADD MESSAGE CONTENTS

#First time Init, Cleans up csv to only have a list of zip codes.
#zipCodes = pd.read_csv('zipCodes/ZipCodes.csv')
#print(zipCodes)
#zipCodes.drop("state_fips", inplace=True, axis=1)
#zipCodes.drop("state", inplace=True, axis=1)
#zipCodes.drop("state_abbr", inplace=True, axis=1)
#zipCodes.drop("county", inplace=True, axis=1)
#zipCodes.drop("city", inplace=True, axis=1)
#print(zipCodes['zipcode'].)

stop = False
URL = "https://www.reddit.com/r/hardwareswap/new/"
print("Connecting to HardWareSwap please wait...")
TIME = 1 #in minutes to refresh
def clean(item):
    #Clean items with no text.
    #Remove BR and DEL
    workingItem = str(item)
    sentenceLen = workingItem.__len__()-1
    i = 0
    while(i < sentenceLen):
        start = 0
        end = sentenceLen
        iahead1 = i + 1
        ibehind1 = i - 1
        if(workingItem[i] == "<") & (workingItem[iahead1] == "d"):
            start = 5
            workingItem = workingItem[start:sentenceLen]
        
        if(workingItem[i] == ">") and (workingItem[ibehind1] == "v"):
            end = i - 5
            workingItem = workingItem[start: end]
        if(workingItem[i] == "<") and (workingItem[iahead1] == "a"):
            return "/"
        i = i + 1
    return workingItem
    

#Generate List of previous posts. Should only contain a max of 10 posts. 
ListOfPreviousPosts = []
while(stop != True):


    def calculate(items):
        listOfMoneyWords = ["bucks", "dollars", "cash", "asking"]
        #print(items)
        numsList = []
        letters = str(items).split()
        nums = ""
        #Iterates through all of the words to find key words or numbers
        for let in letters:
            let = let.lower()
            if let in listOfMoneyWords:
                numsList.append(let)

            if(let.isnumeric() == True):
                numsList.append(let)
            else:
                wordlen = let.__len__()
                i = 0
                while(i < wordlen):
                    if(let[i] == "$"):
                        nums = nums + let[i]
                    if(let[i].isnumeric() == True):
                        nums = nums + let[i]
                    i = i + 1

                if(nums.__len__() != 0):
                    numsword = ''.join(nums)
                    numsList.append(numsword)
                    nums = ""

        #Cleans numbers to only select values that may be a price.
        listMoneyVals = []
        size = numsList.__len__()
        j = 0
        while(j < size):
            oneBehind = j
            oneAhead = j
            if(j != 0) and (j < size - 1):
                oneBehind = j - 1
                oneAhead = j + 1
            if(str(numsList[j]).isnumeric() == False):
                #print("Money Value." + str(numsList[j]))
                listMoneyVals.append(str(numsList[j]))
            if str(numsList[oneBehind]) in listOfMoneyWords or str(numsList[oneAhead]) in listOfMoneyWords:
                #print("Possible Money Value." + str(numsList[j]))
                listMoneyVals.append(str(numsList[j]))
            j = j + 1

        #Get smallest number from values
        sizeOfList = listMoneyVals.__len__()
        k = 0
        #inf val.
        original = 9999999
        itemList = []
        for item in listMoneyVals:
            itemList.append(item)
        #print(itemList)
        


        while(k < sizeOfList):
            word = listMoneyVals[k]
            numbers = re.findall('[0-9]+', word)
            len = numbers.__len__()
            if(len != 0):
                if(int(numbers[0]) < original):
                    original = int(numbers[0])
            
            k = k + 1
        #if(original != 9999999):
        pricesList = []
        if(original != 9999999):
            pricesList.append(original)
            return pricesList

    isprint = False
    page = requests.get(URL)
    #Checks if webpage is offline.
    if(page.status_code != 200):
        print("Reddit hardware Swap is offline")
        time.sleep(120)
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id="SHORTCUT_FOCUSABLE_DIV")
        
        #Find the Corresponding element.
        try:
            #have to test.
            posts = results.find_all("h3", class_="_eYtD2XCVieq6emjKBH3m")
            options = results.find_all("div", class_="_2X6EB3ZhEeXCh1eIVA64XM")
            timeDisplayed = results.find_all("a", class_="_3jOxDPIQ0KaOWpzvSQo-1s")
            links = results.find_all("div", class_="_292iotee39Lmt0MkQZ2hPV")
            linkToPosts = results.find_all("a", class_="SQnoC3ObvgnGjWt90zD9Z")
            postInfo = results.find_all("div", class_="_292iotee39Lmt0MkQZ2hPV")
        except AttributeError:
            print("ERROR")
        
        pricesList = []
        ###PRICE ESTIMATOR
        for postInf in postInfo:
            #print(postInfo)
            txt = str(postInf)
            val1 = txt.find('<p')
            
            #print(val1)
            i = val1
            
            wordsList = []
            wordMaker = []
            try:
                val2 = 0
                val3 = 0
                while True:
                    ahead = i + 1
                    aheadx2 = i + 2
                    
                    if(txt[i] == "<") and (txt[ahead] == "p") and txt[aheadx2] == " ":  
                        val2 = i + 35
                    if(txt[i] == "/") and (txt[ahead] == "p") and txt[aheadx2] == ">":
                        val3 = i - 1  
                        word = txt[val2:val3]
                        word = clean(word)
                        if(word != "/"):
                           wordsList.append(word)
                    
                    
                    i = i + 1
              #      if(txt[i] != " "):
              #          wordMaker.append(txt[i])
              #      if(txt[i] == " "):
              #          wordsList.append(wordMaker)
              #          wordMaker.clear
                
            except IndexError:
                #print()
                void = "do nothing"
            for words in wordsList:
                val = calculate(words)
                #
                if(val != None):
                    pricesList.append(val[0])

        #
        
        ###GETS LINK FOR REDDIT POST
        linkPostsList = []
        for linkToPost in linkToPosts:
            linksToPst = ("https://www.reddit.com" + str(linkToPost.get('href')))
            linkPostsList.append(linksToPst)

        ###GETS LINK FOR IMAGES AND POST TITLE
        postsList = []
        linkList = []
        print(links)
        for linkFound,post in zip(links, posts):
            linky = linkFound
            linky = str(linky)
            val1 = linky.find('href')
            val2 = linky.find('rel=')
            postInfo = (str(post.text))
            if val1 != -1:
                #Gets Link for the images from post info
                size = (val2-2) - (val1+6)
                #Prevents glitches from links where it gets more than link from html data.
                if(size < 150):
                    linkStr = linky[val1+6:val2-2]                
                else:
                    linkStr = "No Link Avaliable"
            #If no link is found
            if val1 == -1:
                linkStr = "No Link Avaliable"
            linkList.append(linkStr)
            postExists = False
            #Checks for Duplicates.
            for items in ListOfPreviousPosts:
                if(items == postInfo):
                    postExists = True
            if(postExists == False): 
                postsList.append(postInfo)
            #Clears out ListOfPosts to prevent overflow.
            ListOfPreviousPosts.insert(0, postInfo)
            if(ListOfPreviousPosts.__len__() > 8):
                while(ListOfPreviousPosts.__len__() > 8 & ListOfPreviousPosts.__len__() != 0):
                    ListOfPreviousPosts.pop()

        ###CALCULATES TIME*********
        timeList = []
        for timePosted in timeDisplayed:
            timeDis = (str(time.strftime('%I:%M:%p')))
            timeList.append(timeDis)
        
        ###DETERMINES IF PERSON IS SELLING BUYING ETC
        optionItems = []
        for option in options:
            lista = ["SELLING", "TRADING", "BUYING", "CLOSED"]
            purchaseOption = (str(option.text))
            if purchaseOption in lista:
                optionItems.append(purchaseOption)
            else:
                isprint = True

        #Data printed here
        for post, option, timeToPrint, linkie, linksToPst, price2 in zip(postsList, optionItems, timeList, linkList, linkPostsList, pricesList):
            if(option == "SELLING"):
                print("Post found at " + timeToPrint + " " + option + " - " + post + "\n Link for images of items sold -> " +
                      linkie + "\n Link to reddit post -> " + linksToPst + "\n Post information -> " + "We estimate price starts at " + str(price2))
                print(" --- ")
                isprint = True
        #verified if program worked. if not it attempts to refresh again. 
        if(isprint == False):
            #DEBUGGING
            #print("Loading")
            #DEBUGGING
            time.sleep(10)
        if(isprint == True):
            #DEBUGGING
            #print("Successful!")
            #DEBUGGING
            time.sleep(TIME*60)
            print("***** Refreshing *****")
        
           
