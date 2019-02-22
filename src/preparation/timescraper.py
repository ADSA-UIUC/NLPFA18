from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import sys


class TimeScraper:

    def __init__(self, homelink='http://time.com'):
        self.homelink = homelink

    def _getPosts(self, topic):
        homelink = self.homelink
        driver = webdriver.Chrome()
        driver.get(homelink + '/' + topic)

        keep_scraping = True
        all_posts = []

        while keep_scraping:

            # get all post links on current page
            content = [x for x in driver.find_elements_by_tag_name('section') if 'content' in x.get_attribute('class')][0]
            headlines = []
            for body in content.find_elements_by_class_name('media-body'):
                for head in body.find_elements_by_class_name('headline'):
                    headlines.append(head)
            post_links = []
            for h in headlines:
                for a in h.find_elements_by_tag_name('a'):
                    post_links.append(a.get_attribute('href'))

            return_link = driver.current_url

            # get post data
            for link in post_links:
                print(link)
                driver.get(link)

                print("checkpoint")

                title = [x.text for x in driver.find_elements_by_tag_name('h1') if 'headline' in x.get_attribute('class')][0]
                timestamp = driver.find_element_by_class_name('published-date').text
                # TODO: add control to change date when posted day of (for consistency)
                print(title, timestamp)

                # stop scraping when post is too old (after small test sets, change 20 to 2019)
                if 'AM' not in timestamp and 'PM' not in timestamp and ' 20' not in timestamp:
                    keep_scraping = False
                    print('early exit')
                    break

                # get other post info

                text = ''
                for p in driver.find_element_by_class_name('article').find_elements_by_tag_name('p'):
                    text += '{} '.format(p.text)

                all_posts.append([timestamp, title, text])

            # go to next page
            driver.get(return_link)
            next = [x.getAttribute('href') for x in driver.find_elements_by_class_name('paginator-link') if x.get_attribute('tag') == 'a'][0]
            driver.get(next)

        ## end while

        return all_posts


    def scrape(self, topics=['health','sports','tech']):
        # for topic in topics:
        #     _getPosts(topic)
        data = self._getPosts(topics[0])
        data.extend(topics[0])
        return pd.DataFrame(data, columns=['timestamp', 'title', 'text', 'topic'])


def main():
    timescraper = TimeScraper()
    timescraper.scrape().to_csv('testhealth.csv')

if __name__ == "__main__":
    sys.exit(main())
