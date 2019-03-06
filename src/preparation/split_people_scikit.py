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
#                 'sentiments': [
#                     anger_value,
#                     ...
#                 ]
#             },
#             ...
#         ],
#         'post_centroids': [
#             [
#                 anger_value,
#                 ...
#             ],
#             ...
#         ]
#     },
#     ...
# }

import json, re, sys, os
import pandas as pd
from pprint import pprint
import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime

class PeopleStorer:
    def __init__(self, data_loc, output_file_json, output_file_csv):
        # defined constants
        self._sentiments_list = ['Anger', 'Fear', 'Joy', 'Sadness', 'Analytical', 'Confident', 'Tentative']
        self._variance_threshold = 0.5


        filenames = os.listdir(data_loc)
        # filter through filenames and make sure to only use doclevel sentiments
        filenames = [data_loc.replace('/_finished', '') + re.sub('\.csv', '_doclevelsentiments.csv', x) for x in filenames]

        self._people_dict = {}
        self._people_df = pd.DataFrame(columns=[
            'source', 'text', 'time',
            'Anger',
            'Fear',
            'Joy',
            'Sadness',
            'Analytical',
            'Confident',
            'Tentative'
        ])

        for x in set(filenames):
            if x.startswith("."): continue
            self._individual_file(x)

        for name in self._people_dict:
            self._calculate_centroids(name)

        self._dump_to_file(output_file_json, output_file_csv)

    def _individual_file(self, filename):
        orig_filepath = filename.replace("sentiments/", "sentiments/_finished/").replace("_doclevelsentiments", "")
        orig_file_reader = pd.read_csv(orig_filepath, encoding="unicode_escape")

        csv_reader = pd.read_csv(filename, encoding="unicode_escape")
        for ind, row in enumerate(csv_reader.iterrows()):
            # need the original file for time of post and post mood
            orig_file_row = orig_file_reader.iloc[ind]
            row = row[1]

            if row['source'] not in self._people_dict:
                self._people_dict[row['source']] = {}
            if 'posts' not in self._people_dict[row['source']]:
                self._people_dict[row['source']]['posts'] = []
            to_add = {
                'time': orig_file_row['date'],
                'text': row['text'],
                # 'mood': orig_file_row['post mood'],
                'sentiments': {name: row[name] for name in self._sentiments_list},
                'forum_name': filename[11:-23] # extract only the subject name from entire filename
            }
            self._people_dict[row['source']]['posts'].append(to_add)

            self._people_df = self._people_df.append(
                {
                    "username": row['source'],
                    "text": to_add['text'],
                    "time": to_add['time'],
                    'Anger': to_add['sentiments']['Anger'],
                    'Fear': to_add['sentiments']['Fear'],
                    'Joy': to_add['sentiments']['Joy'],
                    'Sadness': to_add['sentiments']['Sadness'],
                    'Analytical': to_add['sentiments']['Analytical'],
                    'Confident': to_add['sentiments']['Confident'],
                    'Tentative': to_add['sentiments']['Tentative']
                }, ignore_index=True
            )

    def _calculate_centroids(self, person):
        sentiments = [post['sentiments'] for post in self._people_dict[person]['posts']]
        arr_sentiments = [[i for i in sentiment.values()] for sentiment in sentiments]

        centroids, labels = self._kmeans(arr_sentiments, plot_title=person)
        self._people_dict[person]['num_centroids'] = len(centroids)
        self._people_dict[person]['centroids'] = centroids
        self._people_dict[person]['centroid_labels'] = labels
        # print('finished calculating centroids for', person)


    def _kmeans(self, data, error_threshold=0.1, plot_title=""):
        errors = []
        ks = []
        k = 1

        if (len(data) == 1):
            return data, [0]

        while True:
            kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
            error = kmeans.inertia_
            errors.append(error)
            ks.append(k)
            if error / len(data) < error_threshold:
                break
            k += 1

        # K AGAINST ERROR PLOT TO FIND OPTIMAL K
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # ax.plot(ks, errors)
        # plt.title("k against error for " + plot_title)
        # plt.show()

        return (kmeans.cluster_centers_.tolist(), kmeans.labels_.tolist())


    def _dump_to_file(self, filename_json, filename_csv):
        with open(filename_json, 'w') as f:
            json.dump(self._people_dict, f)
            f.write('\n') # append newline at end

        self._people_df.to_csv(filename_csv, index=False)

    def get_people_array(self):
        return [self._people_dict[person] for person in self._people_dict]

def main():
    now = datetime.now()
    PeopleStorer("sentiments/_finished/", "news.json", "news.csv")
    print('finished creating news.csv, news.json; took: {}'.format(datetime.now() - now))

if __name__ == "__main__":
    sys.exit(main())
