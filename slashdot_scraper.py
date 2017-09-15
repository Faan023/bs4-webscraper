from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import time
from datetime import datetime as dt
from time import gmtime, strftime
import requests

user = input("Please enter your username: ")
pw = input("Please enter your password: ")

def login(user_name, password):
    values = {'unickname': user_name,
             'upasswd': password
             }
    my_url = 'https://slashdot.org/my/login'
    session = requests.session()
    uClient = session.post(my_url, data=values)
    page_html = uClient.content

    page_soup = soup(page_html, 'html.parser')
    session.close()
    containers_u = page_soup.find_all('nav', {'class': 'nav-user'})

    for container in containers_u:
        for span in container.find_all('span'):
            current_user = span.get_text().strip()# I lost about 5 hours because i forgot to strip whitespaces on this ONE text!!! facepalm :-)                   
            if current_user == user_name:
                return (current_user)
            else:
                return ('Unknown user')

while login(user,pw) != user:
    print ( 'Login failed, please enter you login detials again:')
    user = input("Please enter your username: ")
    pw = input("Please enter your password: ")
    
if login(user,pw) == user:
    current_epoch = int(time.time())

    search_date = 'on Saturday August 19, 2017 @09:00AM'

    search_epoch = dt.timestamp(dt.strptime(search_date, "on %A %B %d,  %Y @%H:%M%p"))


    print ('Current epoch: ', current_epoch)
    print ('Search date: ' , search_date)
    print ('Search epog:', search_epoch) # Not too sure about the timestamp format, so I made it a constant. 

    my_url = 'https://slashdot.org/archive'
    uClient = uReq(my_url)

    page_html = uClient.read()

    uClient.close()

    page_soup = soup(page_html, 'html.parser')


    posts = []
    containers = page_soup.find_all('header')


    for header in containers:
        for link in header.find_all('span', {'class':'story-title'}):
            headline = link.get_text()

        for link in header.find_all('span', {'class':'story-byline'}):
                author = (link.get_text())
                author1 = [item.strip() for item in author if str(item)]
                author2 = ("".join(author1).strip('Postedby')) # .strip(date) if date input is in the right format?
                sep = 'on'           
                rest = author2.split(sep, 1)[0] # ToDo : this is just nasty, has to be a better way?
            

    ##    for link in header.find_all('span', {'class':'story-byline'}):
    ##        for a in link.find_all('a'):
    ##            author = (a.get_text())
    ##            authors.append(author) much cleaner, but this way I only get the details if there is an <a> link,twitter link maybe...

        for span in header.find_all('span', {'class':'story-byline'}):
            for time in span.find_all('time'):
                date = time.get_text()
                epoch = dt(1970, 1, 1)
                epoch_time = int((dt.strptime(date, "on %A %B %d,  %Y @%H:%M%p") - epoch).total_seconds())
                
                if epoch_time > search_epoch:
                        posts.append({'Headline': headline,
                              'Author' : rest,
                              'Date': epoch_time})

 
    for i in posts:
        for d in i:
            print(i, d, sep='')
    
