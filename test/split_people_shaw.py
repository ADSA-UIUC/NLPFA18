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

import json
import sys

class PeopleStorer:
    def __init__(self, data_loc, output_file):
        # defined constants
        self._sentiments_list = ['Anger', 'Fear', 'Joy', 'Sadness', 'Analytical', 'Confident', 'Tentative']
        self._variance_threshold = 0.5


        filenames = os.listdir(data_loc)
        # filter through filenames and make sure to only use doclevel sentiments
        self._filenames = [data_loc + x for x in filenames if re.match("^.+[0-9]+_doclevelsentiments\.csv$", x)]
        self._people_dict = defaultdict(defaultdict(list))
        _store_people()
        _dump_to_file(output_file)

    def _store_people(self):
        map(lambda x: _individual_file(x), self._filenames)

    def _individual_file(filename):
        orig_filepath = filename.replace("sentiments", "posts/_finished", 1).replace("doclevelsentiments", "")
        orig_file_reader = csv.reader(open(orig_filepath, 'rb'))
        with open(filename, 'rb') as f:
            csv_reader = csv.reader(f, delimiter=',')
            for index, row in enumerate(csv_reader):
                # need the original file for time of post and post mood
                orig_file_row = orig_file_reader[index]
                self._people_dict[row['username']]['posts'].append({
                    'forum_name': re.findall("(?<=/)[a-zA-Z]+(?=[0-9]+_doclevelsentiments\.csv)", filename)[0],
                    'time': orig_file_row['date'],
                    'text': row['text'],
                    'mood': orig_file_row['post mood'],
                    'sentiments': {name: row[name] for name in self._sentiments_list}})

    def _sentiment_to_num_centroids:
        sentiment_thresholds = []


    def _dump_to_file(self):
        pass

def main():
    PeopleStorer("../data/raw/sentiments/", "../data/processed/people.json")

if __name__ == "__main__":
    sys.exit(main())
