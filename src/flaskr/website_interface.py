import json
from collections import defaultdict
from sklearn.cluster import KMeans
import random

class WebsiteInterface:

    def __init__(self, people_file):
        with open(people_file, 'r') as f:
            self._all_people = json.load(f)

        self._by_forum = defaultdict(list)
        for person in self._all_people:
            for post in self._all_people[person]['posts']:
                self._by_forum[post['forum_name']].append(post)

    def get_n_random_forum_posts(self, forum_name="solonely", n=6):
        self._forum_name = forum_name
        forum_posts = self._by_forum[forum_name]
        post_texts = [post['text'] for post in forum_posts]
        random_posts = random.sample(post_texts, n)
        return random_posts

    def get_actual_groupings(self, groupings):
        n_groups = len(groupings)

        forum_post_sentiments = [list(post['sentiments'].values()) for post in
            self._by_forum[self._forum_name]]

        kmeans = KMeans(n_clusters=n_groups, random_state=0)
        kmeans.fit(forum_post_sentiments)

        cluster_centers = kmeans.cluster_centers_.tolist()
        labels = kmeans.labels_.tolist()

        user_posts = []
        for group in groupings:
            for post in group:
                user_posts.append(post)
        forum_post_texts = [post['text'] for post in
            self._by_forum[self._forum_name]]

        sentiment_order = ['Anger', 'Fear', 'Joy', 'Sadness', 'Analytical', 'Confident', 'Tentative']
        computer_groupings = defaultdict(list)
        for ix, post in enumerate(forum_post_texts):
            for user_post in user_posts:
                if post == user_post and post not in computer_groupings[labels[ix]]:
                    sentiments = forum_post_sentiments[ix]
                    max_sentiment_value = max(sentiments)
                    max_sentiment = sentiment_order[sentiments.index(max_sentiment_value)]
                    to_add = {
                        'text': post,
                        'sentiments': sentiments,
                        'primary_sentiment': max_sentiment,
                        'primary_sentiment_value': max_sentiment_value
                    }
                    computer_groupings[labels[ix]].append(to_add)
        return list([value for key, value in computer_groupings.items()])

def main(people_file, topic):
    interface = WebsiteInterface(people_file)
    print("group the below posts into groups by copy pasting each exact " +\
        "text (without the quotes) on each new line. separate each group " +\
        "by a blank line")
    for ix, random_post in enumerate(\
            interface.get_n_random_forum_posts(topic, 6)):
        print("{} {}".format(ix, random_post))

    human_groupings = [[]]
    i = 0
    while True:
        input_str = input()
        if input_str == "":
            human_groupings.append([])
            i += 1
        elif input_str == "quit":
            computer_groupings = interface.get_actual_groupings(human_groupings)
            print("These are the computer's groupings")
            ix = 0
            for group in computer_groupings:
                for text in computer_groupings:
                    print("group: {} {}".format(ix, text))
                ix += 1
            break
        else:
            human_groupings[i].append(input_str)

if __name__ == "__main__":
    main('../preparation/news.json', 'entertainment')#'../data/processed/people.json')
