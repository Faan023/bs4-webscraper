from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


my_url = 'http://www.imdb.com'
uClient = uReq(my_url)

page_html = uClient.read()

uClient.close()

page_soup = soup(page_html, 'html.parser')

containers = page_soup.find_all('div', {'class':'rhs-row'}, limit=10)
titles = []
posts = []
links = []
rel_dates = []
for div in containers:
    for a in div.find_all('a'):
        redirect = a.get('href')
        title = a.get_text()
        titles.append(title)
        redir_url = my_url + redirect
        uClient = uReq(redir_url)
        redir_page_html = uClient.read()
        uClient.close()
        links.append(redir_url)# follow this link(complete link)


for i in links:
    my_url = (i)
    uClient = uReq(my_url)
    page_html = uClient.read()
    
    page_soup = soup(page_html, 'html.parser')
    containers = page_soup.find_all('div', {'class': 'title_wrapper'})
    uClient.close()

    for container in containers:
        for a in container.find_all('a', {'title': 'See more release dates'}):
            rel_date = a. get_text()
            rel_date1 = [item.strip() for item in rel_date if str(item)]
            rel_date2 = (''.join(rel_date1))
            rel_dates.append (rel_date2)
            
for i,j in zip(titles, rel_dates):
    posts.append({'Title': i,
                'Release date':j
                })
    
print (posts)



                                        
