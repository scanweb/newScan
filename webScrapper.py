#import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
#import ssl
import requests
from datetime import date, timedelta
import datetime
# Import smtplib for the actual sending function
import smtplib
from socket import gaierror

# Import the email modules we'll need
from email.message import EmailMessage

#convert list to string
def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1

# the target we want to open
urls = ['https://www.biospace.com/news/',
        'https://www.biospace.com/news/2/',
        'https://www.biospace.com/news/3/',
        'https://www.biospace.com/news/4/',
        'https://www.biospace.com/news/5/',
        'https://www.biospace.com/news/6/',
        'https://www.biospace.com/news/7/',
        'https://www.biospace.com/news/clinical-trials-phase-i/',
        'https://www.biospace.com/news/clinical-trials-phase-ii/',
        'https://www.biospace.com/news/clinical-trials-phase-iii/',
        'https://www.biospace.com/news/clinical-trials-phase-iv/',
        'https://www.biospace.com/news/fda-approvals/',
        'https://www.biospace.com/news/earnings/']


#open with GET method
allurls = []
headings =[]
for url in urls:
    resp = requests.get(url)
    # http_response 200 means OK status
    if resp.status_code == 200:
        # we need a parser,Python built-in HTML parser
        soup = BeautifulSoup(resp.text, 'html.parser')
        print("URL visited:", url)
        # newsFeed is the list which contains all the text i.e news
        # links = [a['href'] for a in soup.select('a[href]')]
        #loop through all the li attribute and take store in to allArticles
        allArticles = soup.find_all('li', {'class': "cf block lister__item lister__item--article"})
        print('Total Article', len(allArticles))
        print('Articles are: ', allArticles)
        #loop through all articles and find attributes that we care about
        for article in allArticles:
            publishedDate = article.find('p', {'class': "lister__article-date small"})['content']
            publishedDate = publishedDate[0:10]
            publishedDate = datetime.datetime.strptime(publishedDate,'%Y-%m-%d').date()
            titleBlock = article.find('h3',{'class':'lister__header h2'})
            newLink= [a['href'] for a in article.select('a[href]')]
            deepLink = [a['href'][0:a['href'].find("/?s",1,len(a['href']))] for a in article.select('a[href]')]
            #print('Deeplink before:',newLink)
            #print("This is deeplink:", deepLink)
            #print("This is the article", heading)
            #print("this is pulication date", publishedDate)
            #print("this is the link", deepLink)
            today = date.today()
            yesterday = today - timedelta(days = 1)
            #add articles that are published since yesterday
            if publishedDate >= yesterday:
                allurls += deepLink

allurl = list(set(allurls))
print("number of url", len(allurl))
print("URL are:", allurl)

#optimize the process to ignore the articles that has already sent before

with open('allLink.txt') as f:
    linksent = f.read()

allitems=''
allLink=''
for link in allurl:
    #print("I am looking at:", link)
    #if list contains article then request the page else continue
    fullLink = "https://www.biospace.com" + link
    res = requests.get(fullLink)
    #print(fullLink, 'starts with http')
    # if response is 200 then read the page else continue
    if res.status_code == 200:
        eachPage = BeautifulSoup(res.text, 'html.parser')
        text_elements = [t for t in eachPage.find_all(text=True)]
        titleBlock = eachPage.h1.text
        #print('reviewing text',text_elements)
        #print("this is the initial text", text_elements)
        #list of keywords that we care about
        with open('keywords.txt') as f:
            keywords = f.read().splitlines()
        allwords = listToString(text_elements).lower()
        count = 0
        foundKeywords = ""
        for keyword in keywords:
            if (allwords.find(keyword) != -1):
                count += 1
                foundKeywords = foundKeywords+" "+"'"+keyword+"'"
    print('Link looking at: ',fullLink)
    print('Link already sent:', linksent.find(fullLink))
    print('keyWords found:', count)
    if linksent.find(fullLink) == -1 and count !=0:
        item = 'Number of Keywords found:' + str(count) + '\n'+ 'Keywords found: '+foundKeywords +'\n'+ 'Title of Article: '+ titleBlock +'\n'+ fullLink+ '\n'
        allitems += item+ '\n'
        allLink += fullLink+'\n'

print('I read :', allitems == "")
print("Mail content: ", allitems)
if allitems != "":
    print("finally:",allitems)
    port = 465
    smtp_server = "smtp.gmail.com"
    login = "xxxxxxxx@gmail.com"  # paste your login generated by Mailtrap
    password = "######"  # paste your password generated by Mailtrap

    sent_from = 'xxxxxxxx@gmail.com'
    to = [line.rstrip('\n') for line in open('contact.txt')]
    subject = 'Please do needful: Articles with Interested Keywords Found'
    body = "Articles found are below: \n \n" + allitems

    email_text ="From: %s\nTo: %s\nSubject: %s\n\n%s" % (sent_from, [to], subject, body)

    try:
        # Send your message with credentials specified above
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(login, password)
            server.ehlo()
            server.sendmail(sent_from, to, email_text.encode('utf-8'))
    except (gaierror, ConnectionRefusedError):
        # tell the script to report if your message was sent or which errors need to be fixed
        print('Failed to connect to the server. Bad connection settings?')
    except smtplib.SMTPServerDisconnected:
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        print('SMTP error occurred: ' + str(e))
    else:
        print('Sent')
        f = open("allLink.txt","a+")
        f.write(allLink)
        f.close()
else:
    exit()
