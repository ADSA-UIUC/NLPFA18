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
    def __init__(self, data_loc):
        self._filenames = os.listdir(data_loc)
        self._people_dict = {}

    def dump_to_file(self):
        pass

def get_data(folderpath, all_files=True):
    """
    convert data into format:
    [[x1's], [x2's], [x3's], ...] (depending on number of dimensions data is in)
    :param filepath: path to specific file type in format:
    data.frame with columns: "post #", "username", "text", (7 Watson API output emotions)
    """
    filenames = os.listdir(folderpath)
    all_values = pd.DataFrame()
    for filename in filenames:
        if not re.match(".+_sentencelevelsentiments\.csv", filename):
            continue
        all_data = pd.read_csv(folderpath + filename)
        # get the appropriate columns' values
        select_vals = all_data.iloc[:,all_data.columns.get_loc('Anger'):]
        all_values = all_values.append(select_vals)
    # required format is all values of 1 dimension are in same array
    return all_values.values.T.tolist()


# INCLUDE MAP FUNCTION SOMEWHERE??

def main():
    '''
    ALGORITHM (incorporate into get_data)
    go through original data csv (get post info) then go through sentiments
    file of same name(+_doclevelsentiments) to get sentiment data


    people_dict = {}

    for file in folder:
        for row in csv:  # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.iterrows.html#pandas.DataFrame.iterrows
            if person in people_dict:
                people_dict[person][posts].append(post_info_dict)
                people_dict[person][post_centroids].append(centroids)  # (TODO: format of centroids = ?)
            else:
                people_dict[person] = {}
                people_dict[person][posts] = post_info_dict
                people_dict[person][post_centroids] = centroids

    with open('people.json', 'w') as outfile:
        json.dump(people_dict, outfile)
    '''


if __name__ == "__main__":
    sys.exit(main())
