# stock seacher / analysis
# elon monitor, random stock picker
# Stock position simulator
# % increase expected? take profit levels

#Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pyautogui
import re
import math

#Request
ticker = input("Ticker: ")
data = input("Full Analysis (y/n): ")
if data == "n":
    data = input("news OR info OR comunity: ")
price = 0.0

def yahoo():
    #Setup
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    #Fetch yahoo
    driver.get("https://finance.yahoo.com/quote/" + ticker.upper())
    time.sleep(3)
    #driver.find_element(By.XPATH, "//*[@id='myLightboxContainer']/section/button[1]").click()
    page = driver.find_element(By.XPATH, "/html/body").text
    #BASICS
    basics = page[page.find("Bid"):page.find("EPS")]
    #CURRENT PRICE
    current = basics[basics.find("Bid")+4:basics.find(" x ")]
    if current == "0.00":
        current = basics[basics.find("Ask")+4:findnth(basics, "x", 1)-1]
    global price
    price = float(current)
    #MARKET CAP
    cap = page[(page.find("Market Cap") + 11):page.find("Beta")]
    if cap.find("M") > 1:
        cap = (float(cap[0:cap.find("M")]) * 1000000)
    elif cap.find("B") > 1:
        cap = (float(cap[0:cap.find("B")]) * 1000000000)
    elif cap.find("T") > 1:
        cap = (float(cap[0:cap.find("T")]) * 1000000000000)
    #RETURN
    print("\n" + "\n" +"YAHOO FINANCE:" + "\n" + "Basics:" + "\n" + basics)
    #BASIC EVALUATION
    basicEval = page[page.find("1y Target"):page.find("View details")]
    print("Basic Evaluation:" + "\n" + basicEval)
    #GET OUTSTANDING
    driver.get("https://finance.yahoo.com/quote/" + ticker.upper() + "/key-statistics")
    page = driver.find_element(By.XPATH, "/html/body").text
    share = page[(page.find("Shares Outstanding 5") + 20):page.find("Implied")+1]
    if share.find("M") > 1:
        share = (float(share[0:share.find("M")]) * 1000000)
    elif share.find("B") > 1:
        share = (float(share[0:share.find("B")]) * 1000000000)
    elif share.find("T") > 1:
        share = (float(share[0:share.find("T")]) * 1000000000000)
    else:
        share = "N/A"
    #FAIR SHARE PRICE
    if share != "N/A":
        fair = float(cap/float(share))
        fairPrint = str(fair)
        fairPrints = fairPrint.find(".")
        fairPrint = str(fairPrint[0:fairPrints+3])
    else:
        fairPrint = "N/A"
    print("\n" + "PERSONAL EVALUATIONS:" + "\n" + "Fair Share Price: $" + fairPrint)
    #RESULTS
    if fairPrint != "N/A":
        if fair > float(current):
            result = "Undervalued by: $" + (str(str(fair-float(current)))[0:(str(fair-float(current)).find(".")+3)])
        elif fair < float(current):
            result = "Overvalued by: $" + (str(str(float(current)-fair))[0:(str(float(current)-fair).find(".")+3)])
        else:
            result = "Calculus: error"
        print(result)
    driver.close()

def yahooNoPrint():
    #Setup
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    #Fetch yahoo
    driver.get("https://finance.yahoo.com/quote/" + ticker.upper())
    time.sleep(3)
    #driver.find_element(By.XPATH, "//*[@id='myLightboxContainer']/section/button[1]").click()
    page = driver.find_element(By.XPATH, "/html/body").text
    #BASICS
    basics = page[page.find("Bid"):page.find("EPS")]
    #CURRENT PRICE
    current = basics[basics.find("Ask")+4:findnth(basics, "x", 1)-1]
    if current == "0.00":
        current = basics[basics.find("Bid")+4:basics.find(" x ")]
    global price
    price = float(current)
    driver.close()

def reddit():
    #Set up
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    good = 0
    bad = 0
    good_words = ['BUY', 'UP', 'GOOD', 'HOLD', 'HODL', 'BUYING']
    bad_words = ['SELL', 'SELLING', 'DOWN', 'SELL NOW', 'TAKE PROFIT', 'BAD', 'FRAUD', 'DROP']
    z = 0

    #Search
    driver.get("https://www.reddit.com/search/?q=" + ticker)
    searchP = driver.find_element(By.XPATH,"/html/body").text.upper()
    while z < len(good_words):
        good = good + searchP.count(good_words[z])
        z = z + 1
    z = 0
    while z < len(bad_words):
        bad = bad + searchP.count(bad_words[z])
        z = z + 1
    z = 0
    print("\n" + "\n" + "REDDIT TALK:" +"\n" + "Good things: " + str(good) + "\n" + "Bad things: " + str(bad) + "\n" + "Total: " + str(good-bad))
    driver.close()

def findnth(string, substring, n):
   parts = string.split(substring, n + 1)
   if len(parts) <= n + 1:
      return -1
   return len(string) - len(parts[-1]) - len(substring)

def insider():
    #Set up
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    good = 0
    bad = 0
    good_words = ['BUY']
    bad_words = ['SELL']
    z = 0

    #Search
    driver.get("https://www.benzinga.com/sec/insider-trades/search/index?company_ticker=" + ticker)
    time.sleep(3)
    #driver.find_element(By.XPATH, "//*[@id='myLightboxContainer']/section/button[1]").click()
    search = driver.find_element(By.XPATH,"/html/body").text
    insiderTotal = search[0:2000]
    while z < len(good_words):
        good = good + insiderTotal.count(good_words[z])
        z = z + 1
    z = 0
    while z < len(bad_words):
        bad = bad + insiderTotal.count(bad_words[z])
        z = z + 1
    z = 0
    print("\n" + "\n" + "INSIDER TRADING:" +"\n" + "Buys: " + str(good) + "\n" + "Sells: " + str(bad) + "\n" + "Total: " + str(good-bad))
    driver.close()

def alpha():
    #Set up
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--headless")
    options.add_argument("--enable-javascript")
    driver = webdriver.Chrome(options=options)

    #Search analysis
    driver.get("https://seekingalpha.com/symbol/" + ticker + "/analysis")
    time.sleep(3)
    search = driver.find_element(By.XPATH,"/html/body").text
    search = re.sub("Comment", "Comments", search)
    search = re.sub("Commentss", "Comments", search)
    analT = search[search.find("Select Date")+11:findnth(search, "Comments", 6)]
    print("\n" + "\n" + "STOCK NEWS:")
    while analT.find("Comments") > 0:
        print(analT[0:analT.find("Comments")])
        analT = analT[analT.find("Comments")+8 :]
    driver.close()

def technicals():
    #Set up
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    print("\n" + "\n" + "TECHNICAL INFORMATION:")

    #Search
    driver.get("https://stockcharts.com/freecharts/symbolsummary.html?sym=" + ticker)
    #RSI
    rsi = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/div[3]/div[2]/div/div[2]/table/tbody/tr[10]/td[2]").text
    if float(rsi) < 30:
        rsiAnal = "Undervalued- BUY"
    elif float(rsi) > 70:
        rsiAnal = "Overvalued- SELL"
    else:
        rsiAnal = "Fair RSI"
    print("RSI: " + rsi + "   " + rsiAnal)
    #institutions
    inst = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/div[3]/div[1]/div/div[2]/table/tbody/tr[10]/td[2]").text
    print("% Held by Institutions: " + inst + "%")
    #Performance
    Fday = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/div[3]/div[2]/div/div[2]/table/tbody/tr[4]/td[2]").text
    Omonth = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/div[3]/div[2]/div/div[2]/table/tbody/tr[5]/td[2]").text
    Tmonths = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/div[3]/div[2]/div/div[2]/table/tbody/tr[6]/td[2]").text
    Smonths = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/div[3]/div[2]/div/div[2]/table/tbody/tr[7]/td[2]").text
    year = driver.find_element(By.XPATH,"/html/body/div[2]/div[3]/div/div[3]/div[2]/div/div[2]/table/tbody/tr[9]/td[2]").text
    print("5-Day: " + Fday)
    print("1-Month: " + Omonth)
    print("3-Months: " + Tmonths)
    print("6-Months: " + Smonths)
    print("Year: " + year)
    driver.close()


def risk(accountSize, riskLevel, confidence, pos, direction):
    #Setup
    yahooNoPrint()
    accountSize = float(accountSize)
    riskLevel = int(riskLevel)
    confidence = int(confidence)
    pos = float(pos)
    print("\n" + "\n" + "POSITION SIZER:")
    
    #Risk Factor
    if pos < price:
        return()
    if riskLevel == 1:
        riskSize = accountSize * 0.01
    elif riskLevel == 2:
        riskSize = accountSize * 0.02
    else:
        riskSize = accountSize * 0.03

    # Info Math
    mostShares = math.floor(pos/price)
    normShares = math.floor(mostShares * 0.45)
    lowShares = math.floor(mostShares * 0.2)
    if lowShares == 0:
        print("Not enough free money for good transaction.")
        return()

    #Long Position
    if direction == "Long" or direction == "long":
        # Give 3 position options
        positionHigh = ("HIGH: Shares: " + str(mostShares) + "   Cost: $" + str(round((mostShares*price), 2)) + "   Stop Loss: $" + str(round((price - (riskSize/mostShares)), 2)))
        positionNormal = ("NORMAL: Shares: " + str(normShares) + "   Cost: $" + str(round((normShares*price), 2)) + "   Stop Loss: $" + str(round((price - (riskSize/normShares)), 2)))
        positionLow = ("LOW: Shares: " + str(lowShares) + "   Cost: $" + str(round((lowShares*price), 2)) + "   Stop Loss: $" + str(round((price - (riskSize/lowShares)), 2)))
        
    #Short Position
    if direction == "Short" or direction == "short":
        # Give 3 position options
        positionHigh = ("HIGH: Shares: " + str(mostShares) + "   Cost: $" + str(round((mostShares*price), 2)) + "   Stop Loss: $" + str(round((price + (riskSize/mostShares)), 2)))
        positionNormal = ("NORMAL: Shares: " + str(normShares) + "   Cost: $" + str(round((normShares*price), 2)) + "   Stop Loss: $" + str(round((price + (riskSize/normShares)), 2)))
        positionLow = ("LOW: Shares: " + str(lowShares) + "   Cost: $" + str(round((lowShares*price), 2)) + "   Stop Loss: $" + str(round((price + (riskSize/lowShares)), 2))) 

    #Return
    if confidence >= 85:
        value = "High"
    elif confidence <= 25:
        value = "Low"
    else:
        value = "Normal"
    print("Recomend: " + value + "  Current $" + str(price) + "   Max Loss $" + str(riskSize))
    print(positionHigh)
    print(positionNormal)
    print(positionLow)
    ques = input("Simulate profit?(y/n): ")
    if ques == "y":
        f = float(input("Target Price: $"))
        plan = input("Plan (e.x. HIGH): ")
        if plan == "HIGH" or plan == "high":
            prof = round(((f-price)*mostShares), 2)
        elif plan == "LOW" or plan == "low":
            prof = round(((f-price)*lowShares), 2)
        elif plan == "NORMAL" or plan == "normal":
            prof = round(((f-price)*normShares), 2)
        else:
            prof = "N/A"
        print("Target Profit for Selected Plan: $" + str(abs(prof)))


if data == "info" or data == "y":
    yahoo()
if data == "comunity" or data == "y":
    reddit()
if data == "news" or data == "y":
    insider()
if data == "news" or data == "y":
    alpha()
if data == "info" or data == "y":
    technicals()
riskQ = input("\n" + "Get Position Size?(y/n): ")
if riskQ == "y":
    a = input("Account Size: $")
    b = input("Level of Risk Willing to Take (1-3): ")
    c = input("Confidence Level %: ")
    d = input("Max Amount of Free Money for Trade: $")
    e = input("Long or Short?: ")
    risk(a, b, c, d, e) 
