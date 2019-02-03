# use map to call same function on all the different sentencelevelsentiment csv's
# add to single database (dict?) of every person
# find way to store it in a file so it can be accessed + appended to later
# calculate a variance value for each person to determine how many centroids
# will be necessary to fully capture data

# inside json file??
# people_dict = {
#     'person1': {
#         'posts': [
#             {
#                 'forum_name': "",
#                 'time': "",
#                 'text': "",
#                 'mood': "",
#                 'keyword': "",
#                 'sentiments': {
#                     'anger': ,
#                     ...
#                 }
#             },
#             ...
#         ],
#         'post_centroids': [
#             {
#                 'anger': ,
#                 ...
#             },
#             ...
#         ]
#     },
#     ...
# }

import json, re, sys, os
import pandas as pd
from pprint import pprint
import numpy as np
from kmeans import kmeans
import matplotlib.pyplot as plt

class PeopleStorer:
    def __init__(self, data_loc, output_file):
        # defined constants
        self._sentiments_list = ['Anger', 'Fear', 'Joy', 'Sadness', 'Analytical', 'Confident', 'Tentative']
        self._variance_threshold = 0.5


        filenames = os.listdir(data_loc)
        # filter through filenames and make sure to only use doclevel sentiments
        filenames = [data_loc.replace('posts/_finished', 'sentiments') + x.replace('.csv', '_doclevelsentiments.csv') for x in filenames]

        self._people_dict = {}
        for x in filenames:
            self._individual_file(x)
        
        for name in self._people_dict:
            self._calculate_centroids(name)

        self._dump_to_file(output_file)

    def _individual_file(self, filename):
        orig_filepath = filename.replace("sentiments", "posts/_finished", 1).replace("_doclevelsentiments", "")
        orig_file_reader = pd.read_csv(orig_filepath)

        csv_reader = pd.read_csv(filename)
        for ind, row in enumerate(csv_reader.iterrows()):
            # need the original file for time of post and post mood
            orig_file_row = orig_file_reader.iloc[ind]
            row = row[1]

            if row['username'] not in self._people_dict:
                self._people_dict[row['username']] = {}
            if 'posts' not in self._people_dict[row['username']]:
                self._people_dict[row['username']]['posts'] = []
            to_add = {
                'forum_name': re.findall("(?<=/)[a-zA-Z0-9]+?(?=[0-9]+_doclevelsentiments\.csv)", filename)[0],
                'time': orig_file_row['date'],
                'text': row['text'],
                # 'mood': orig_file_row['post mood'],
                'sentiments': {name: row[name] for name in self._sentiments_list}}
            self._people_dict[row['username']]['posts'].append(to_add)


    def _calculate_centroids(self, person):
        sentiments = [post['sentiments'] for post in self._people_dict[person]['posts']]
        arr_sentiments = [[i for i in sentiment.values()] for sentiment in sentiments]
        each_sentiment = np.array(arr_sentiments).T.tolist()

        num_centroids, centroids = self._kmeans(each_sentiment, plot_title=person)
        self._people_dict[person]['num_centroids'] = num_centroids
        self._people_dict[person]['centroids'] = centroids
        print('finished calculating centroids for', person)


    def _kmeans(self, data, plot_title=""):
        errors = []
        ks = []
        for k in range(1, 10):
            kmeans_obj = kmeans(data, k=k, display_dims=0, plot_title=plot_title)
            finished, error = kmeans_obj.run(n=20, error_threshold=0.4, display_every=5)
            errors.append(error)
            ks.append(k)
            if finished: break

        # K AGAINST ERROR PLOT TO FIND OPTIMAL K
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # ax.plot(ks, errors)
        # plt.title("k against error for " + str(plot_title))
        # plt.show()

        return (k, kmeans_obj.get_centers())


    def _dump_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self._people_dict, f)

    def get_people_array(self):
        return [self._people_dict[person] for person in self._people_dict]

def main():
    PeopleStorer("../data/raw/posts/_finished/", "../data/processed/people.json")

if __name__ == "__main__":
    sys.exit(main())
