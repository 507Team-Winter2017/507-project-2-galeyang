#proj2.py

import urllib.request, urllib.error, urllib.parse
import json, ssl, re
from bs4 import BeautifulSoup


#### Problem 1 ####
print('\n*********** PROBLEM 1 ***********')
print('New York Times -- First 10 Story Headings\n')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'http://nytimes.com'
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

for heading in soup.find_all(class_="story-heading")[:10]: 
    if heading.a: 
        print(heading.a.text.replace("\n", " ").strip())
    else: 
        print(heading.contents[0].strip())



#### Problem 2 ####
print('\n*********** PROBLEM 2 ***********')
print('Michigan Daily -- MOST READ\n')

url2 = 'https://www.michigandaily.com/'
html2 = urllib.request.urlopen(url2, context=ctx).read()
soup2 = BeautifulSoup(html2, 'html.parser')

most_read = soup2.find_all(class_="view-most-read")[0]
# most_read = soup2.find_all('div', {'class': lambda x: x and 'view-most-read' in x.split()})

for heading in most_read.find_all('a'): 
    print(heading.text)


#### Problem 3 ####
print('\n*********** PROBLEM 3 ***********')
print("Mark's page -- Alt tags\n")

url3 = 'http://newmantaylor.com/gallery.html'
html3 = urllib.request.urlopen(url3, context=ctx).read()
soup3 = BeautifulSoup(html3, 'html.parser')

for img in soup3.find_all('img'): 
    if img.has_attr('alt'):
        print (img.get('alt'))
    else:
        print ('No alternative text provided!')


#### Problem 4 ####
print('\n*********** PROBLEM 4 ***********')
print("UMSI faculty directory emails\n")

url_root = 'https://www.si.umich.edu'
email_count = 0

has_next_page = True
current_url = url_root + '/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4'

while has_next_page:
    faculty_email_list = []
    html4_current = urllib.request.urlopen(current_url, context=ctx).read()
    soup4_current = BeautifulSoup(html4_current, 'html.parser')

    for f in soup4_current.find_all(class_='field-name-contact-details'): 
        faculty_url = url_root + f.find('a').get('href') 
        html_faculty_page = urllib.request.urlopen(faculty_url, context=ctx).read()
        soup4_faculty_page = BeautifulSoup(html_faculty_page, 'html.parser')
        field_email = soup4_faculty_page.find(class_='field-name-field-person-email')
        faculty_mailto = field_email.find('a').get('href')
        faculty_email = re.findall(r'mailto:(.*)', faculty_mailto) 
        faculty_email_list.append(faculty_email[0])

    for email in faculty_email_list:
        email_count += 1
        print (str(email_count) + " " + email)

    #detect whether the next page exist
    if soup4_current.find(class_='pager-next').a:
        has_next_page = True
        next_page_url = url_root + soup4_current.find(class_='pager-next').a.get('href')

        current_url = next_page_url

    else:
        has_next_page = False

    