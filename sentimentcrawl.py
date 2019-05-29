'''

Description: Webscraping Baidu!

# browser.get(search_url + search_text)  # open browser
# request = requests.get(url + search_text)  # get a response object, has .text property
# browser.quit()

'''

from selenium import webdriver
from urllib.request import urlopen
import requests
import bs4
import os
import time

base_url = r'http://c.tieba.baidu.com'
search_url = base_url + r'/f?ie=utf-8&kw='
post_url_max_length = 30

# browser = webdriver.Chrome(r'C:\Program Files\Chromedriver\chromedriver.exe')
# browser.get(base_url)

print()
print('Welcome to Baidu Tieba Scraper!')
print('Search for games using keywords to view all comments in all tieba')

while True:
    print('Menu')
    print('0 - Exit')
    print()

    # 1. Input keywords
    search_text = input('>> What would you like to search for? ')

    if search_text.strip() == '0':
        break

    else:
        search_text.replace(' ', '')
        request = urlopen(search_url + search_text).read().decode('utf8')
        soup = bs4.BeautifulSoup(request, 'lxml')
        forums = soup.select('a[href*=/p/]')
        forums_list = []

        with open('tieba_list_forums.csv', 'w', encoding='utf-8') as f:
            headers = 'forum\n'
            f.write(headers)

            count = 0
            for forum in forums:
                print(str(count) + ': ' + forum.text)
                href_value = forum.get('href')
                if (len(href_value) <= post_url_max_length):
                    forums_list.append(href_value)
                    f.write(forum.text.replace(',', '|') + '\n')
                    count += 1

        # 2. Forum selection
        choice = int(input('Choose a forum: '))
        forum_url = (
            base_url if forums_list[choice][1] is 'p' else 'http:') + forums_list[choice]
        forum_url = 'http://c.tieba.baidu.com/p/6094373794'
        print("forum_url: ", forum_url)

        request = urlopen(forum_url).read().decode('utf8')
        soup = bs4.BeautifulSoup(request, 'lxml')
        posts = soup.select('div[class*=l_post]')

        with open('tieba_list_posts.csv', 'w', encoding='utf-8') as f:
            headers = 'username,user_link,post_description\n'
            f.write(headers)

            for index, post in enumerate(posts):

                user = post.select('a[class*=p_author_name]')
                username = user[0].text.strip()
                user_link = user[0].get('href')

                post_desription = post.select(
                    'div[class*=d_post_content]')[1].text.strip().replace(',', '|')
                post_endings = post.select('span[class*=tail-info]')
                date = post_endings[len(post_endings)-1].text.strip()

                print('{0}: {1}, {2}, {3}, {4}\n'.format(
                    str(index), date, username, user_link, post_desription))

                f.write('{0},{1},{2}，{3}\n'.format(
                    date, username, user_link, post_desription))

    choice = int(input("Another round? 0 = exit"))
    if (choice is 0):
        break

print('Goodbye!')
