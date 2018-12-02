###
#
#   Thread Scraper Object (From Shaw's code)
#   TODO: get more data? (i.e. likes/hugs)
#
###


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime


# Actually a THREAD scraper
def _mentalHealthThreadScraper(url):
    forum_html = requests.get(url)
    forum_json = forum_html.text

    forum_soup = BeautifulSoup(forum_json, 'html.parser')

    users_posts = []
    # get each post
    for post in forum_soup.find_all("li", "postbitlegacy postbitim postcontainer old"):
        # find the username of the poster
        post_user = post.find("div", {"class": "userinfo"})

        username_html = post_user.find("strong")

        # if username is not in <strong></strong> tags then this found users who liked
        other_username_html = post_user.find("a")
        users_who_liked = []
        if other_username_html is not None:
            users_who_liked.append(other_username_html.text)

        # finds the mood of the post
        post_mood_class = post.find("dd", {"class": "vmood-dd-legacy"})
        post_mood = "None"
        if post_mood_class is not None:
            post_mood_image = post_mood_class.find("img")
            post_mood = post_mood_image['alt']

        # get poster
        if username_html is not None:
            username = username_html.text
        else:
            username = post_user.find("span", {"class": "username guest"}).text

        # the post rather than the poster
        post_html = post.find("blockquote", {"class": "postcontent restore "})

        # find date of post
        time_str = post.find("span", "date").text
        time_str = re.sub(u'\xa0', u' ', time_str)
        time_obj = datetime.strptime(time_str, "%d-%m-%y, %H:%M")

        # quoted someone else
        quote_author_html = post_html.find("div", {"class": "bbcode_postedby"})
        if quote_author_html is not None:
            quote_author = quote_author_html.find("strong").text
        else:
            quote_author = None

        # text without links or quotes
        if post_html.find("a") is not None:
            # post.contents will give me the "contents" of the post, which means
            # everything without the <div> tag can be thrown away, and everything
            # with the link we can keep the text for

            # first 2 elements are the '\n' and the <div></div> tag
            post_text = ""
            for content in post_html.contents:
                if content.string is not None:
                    post_text += content.string
        else:
            post_text = post_html.text

        # edit out any '\n' s
        post_final = re.sub("\\n", "", post_text).encode('utf-8', 'replace')

        users_posts.append([time_obj, username, post_final, quote_author, post_mood])

    return users_posts
    
'''
def getMaxPages(url):
    forum_html = requests.get(url)
    forum_json = forum_html.text

    forum_soup = BeautifulSoup(forum_json, 'html.parser')

    page_button = forum_soup.find("a", {"id": "yui-gen6"}).text
    return int(page_button[10:])
'''
def getMaxPosts(url):
    forum_html = requests.get(url)
    forum_json = forum_html.text

    forum_soup = BeautifulSoup(forum_json, 'html.parser')

    page_button = forum_soup.find("div", {"id": "threadpagestats"}).text
    # parse by word, get last word
    return int(page_button[10:])

def getNPosts(threadnum=97215, n=50):
    numPosts = 0
    posts = []
    pagenum = 1
    maxPages = getMaxPages('https://www.mentalhealthforum.net/forum/thread{}.html'.format(threadnum))

    while numPosts < n and pagenum <= maxPages:
        url = 'https://www.mentalhealthforum.net/forum/thread{}-{}.html'.format(threadnum, pagenum)
        newPosts = _mentalHealthThreadScraper(threadnum, pagenum)
        for post in newPosts:
            posts.append(post)
        pagenum += 1
        numPosts += len(newPosts)

    return pd.DataFrame(posts, columns=['date', 'username', 'post content', 'quoted user', 'post mood'])
