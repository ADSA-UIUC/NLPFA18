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
driver.get('https://www.mentalhealthforum.net/forum/forum299.html')

content_container = driver.find_element_by_id_name('forums')
experience_forums = content_container.find_elements_by_tag_name('id')[0]
forum_elements = experience_forums.find_element_by_class_name('forumtitle')

forum_links = []
forum_titles = []
