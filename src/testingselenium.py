'''
PSEUDO CODE ON GOOGLE DOC IN SHARED NLP FOLDER
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threadscraper
import re

def _mentalHealthForumScraper(string link='https://www.mentalhealthforum.net/forum/forum299.html'):
    driver = webdriver.Chrome()
    # Mental Health Experiences Forum
    driver.get("https://www.mentalhealthforum.net/forum/forum299.html")

    threadstats = driver.find_elements_by_class_name("threadstats")
    replies = threadstats[0].find_elements_by_tag_name("a")
    replies[0].click()

    total_threads = 0
    #### WHILE (for pages, if necessary) ####

    # Store Return Link
    return_link = driver.current_url

    # Get threads
    all_threads = driver.find_element_by_class_name('threads')
    threads = driver.find_elements_by_class_name('threadbit')

    for i in range(len(threads)):
        # Get threads
        all_threads = driver.find_element_by_class_name('threads')
        threads = driver.find_elements_by_class_name('threadbit')
        thread = threads[i]

        # remove stickies (check for prefix)
        prefixes = thread.find_elements_by_class_name('prefix')
        if len(prefixes) > 0:
            if prefixes[0].text == 'Sticky:':
                print('SKIPPING STICKY')
                continue;
            else:
                print('UNEXPECED PREFIX', prefixes[0].text)


        # check number of replies
        stats = thread.find_element_by_class_name('threadstats')
        replies_text = (stats.find_elements_by_tag_name('li')[0]).text
        num_replies = int(replies_text[9:].replace(',', ''))
        if num_replies < 150:
            break

        title = thread.find_element_by_class_name('title')
        print(title.text)
        print(num_replies)
        total_threads += 1

        # get thread info before clicking
        num_posts = 100
        forum_id = thread.get_attribute('id')[7:]
        forum_title = (re.sub(r'\W+', '', title.text)).lower()
        print(forum_title)

        # scrape thread
        title.click()
        threadscraper.getNPosts(forum_id, num_posts).to_csv('data/' + forum_title + str(num_posts) + '.csv')
        print(forum_title, 'saved')

        # return to forum page
        driver.get(return_link)

    #### END WHILE ####

    driver.close()
