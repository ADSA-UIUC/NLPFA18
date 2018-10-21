###
#
#   FROM GOOGLE COLAB Dataset_creation.ipynb
#   Edit according to comment at bottom of testingselenium.py
#   TODO: change output path of csv files
#
###

import threadscraper

forum_ids = [97215, 186460, 30827, 188400]
path = "./data"
output_files = ['singlesentence', 'mamistruggling', 'battlingdepressionnomeds', 'relationshipproblems']
num_posts = 100

for forum_id, output_file in zip(forum_ids, output_files):
    threadscraper.getNPosts(forum_id, num_posts).to_csv(output_file + str(num_posts) + '.csv')

