import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def main():
    with open('../data/processed/people.json', 'r') as f:
        people_json = json.load(f)

    # could have formatted this better in the first place, but each person 
    # is a different property in the json file for now. so turn back into
    # array for easy access
    people_arr = [people_json[person] for person in people_json]

    average = np.mean([len(person['posts']) for person in people_arr])
    print("average num sentences: " + str(average))

    all_post_lengths = [len(person['posts']) for person in people_arr]
    print("number of posts made by each person, sorted")
    print(sorted(all_post_lengths))

    pca_visualize_posts('bulbie', pca_dims=2)

def pca_visualize_posts(person_name, pca_dims=0):
    person = person_json[person_name]

    post_objs = person['posts']
    sentiments_objs = [post['sentiments'] for post in post_objs]
    all_sentiments = [sentiment.values() for sentiment in sentiment_objs]
    centroids = person['centroids']

    # pca all the points at once to make sure everything is the same latent space
    all_points_to_pca = all_sentiments + centroids

    pca = PCA(n_components=pca_dims)
    pca.fit(all_points_to_pca)
    components = pca.components_

    


if __name__ == "__main__":
    main()