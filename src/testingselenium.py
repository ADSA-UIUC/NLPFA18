from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
# Mental Health Experiences Forum
driver.get("https://www.mentalhealthforum.net/forum/forum299.html")

# Get threads
threads = driver.find_elements_by_class_name('title')
print(threads[4].text)  # must do this before click
threads[4].click()


'''
PSEUDO CODE FOR MAIN (note difference between forums and threads)
threadscraper might need minor alterations, but should be fine


Make list of forums to scrape (hardcode for now)

for each forum:

    while (page is not end (or max)):
    
        threads = driver.find_elements_by_class_name('title')
        
        for each thread:
            title = thread.text
            scrape thread 
            save to file
            
        click next page button


'''


driver.close()