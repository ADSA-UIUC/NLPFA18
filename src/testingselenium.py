'''
PSEUDO CODE ON GOOGLE DOC IN SHARED NLP FOLDER
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
# Mental Health Experiences Forum
driver.get("https://www.mentalhealthforum.net/forum/forum299.html")

threadstats = driver.find_elements_by_class_name("threadstats")
replies = threadstats[0].find_elements_by_tag_name("a")
replies[0].click()

total_threads = 0
#### WHILE ####

# Store Return Link
return_link = driver.current_url

# Get threads
all_threads = driver.find_element_by_class_name('threads') # still leaves stickies
threads = driver.find_elements_by_class_name('threadbit')[1:]

for thread in threads:
    # check number of replies
    stats = thread.find_element_by_class_name('threadstats')
    replies_text = (stats.find_elements_by_tag_name('li')[0]).text
    num_replies = int(replies_text[9:].replace(',', ''))
    if num_replies < 150:
        break

    title = thread.find_element_by_class_name('title')
    print(title.text)
    print(num_replies)
    total_threads++

    title.click()
    # scrape thread
    driver.get(return_link)

#### END WHILE ####

driver.close()
