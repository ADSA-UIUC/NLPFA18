###
#
#   FROM GOOGLE COLAB Dataset_creation.ipynb
#   Edit according to comment at bottom of testingselenium.py
#   TODO: change output path of csv files
#
###
''' (old code for initial datasets)
import threadscraper

forum_ids = [97215, 186460, 30827, 188400]
path = "./data"
output_files = ['singlesentence', 'mamistruggling', 'battlingdepressionnomeds', 'relationshipproblems']
num_posts = 100

for forum_id, output_file in zip(forum_ids, output_files):
    threadscraper.getNPosts(forum_id, num_posts).to_csv(output_file + str(num_posts) + '.csv')
'''


import testingselenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


forum_home = 'https://www.mentalhealthforum.net/forum/'

driver = webdriver.Chrome()
# Mental Health Experiences Forum
driver.get(forum_home)

content_container = driver.find_element_by_id('forums')
experience_forums = content_container.find_elements_by_tag_name('li')[0]
forum_elements = experience_forums.find_elements_by_class_name('forumtitle')[1:]
# TODO: remove hard coded [1:] (figure why getting extra link)

forum_links = []
forum_titles = []

for element in forum_elements:
    a = element.find_element_by_tag_name('a')
    forum_links.append(a.get_attribute('href'))
    forum_titles.append(a.text)


while True:
    print('------ COMMAND OPTIONS ------')
    for i in range(len(forum_titles)):
        print(i, ':', forum_titles[i])
    print('q : quit program')
    print('a : all')
    print('-----------------------------')

    user_input = input()

    if user_input == 'q':
        break
    elif user_input == 'a':
        print('scraping all')
        for i in range(len(forum_titles)):
            print('scraping', forum_titles[i])
            print('link: ', forum_links[i])
            testingselenium._mentalHealthForumScraper(forum_links[i])
    else:
        selection = int(user_input)
        if selection >= len(forum_links) or selection < 0:
            print('invalid input\n')
        else:
            print('scraping', forum_titles[selection])
            print('link: ', forum_links[selection])
            testingselenium._mentalHealthForumScraper(forum_links[selection])
