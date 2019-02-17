import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import mplcursors
from collections import defaultdict

def main():
    with open('../data/processed/people.json', 'r') as f:
        people_json = json.load(f)

    # could have formatted this better in the first place, but each person
    # is a different property in the json file for now. so turn back into
    # array for easy access

    ### RANDOM STATISTICS. FOLLOW FORMAT IF YOU NEED TO FIND OTHER STATS


    people_arr = [people_json[person] for person in people_json]

    post_lens = [len(person['posts']) for person in people_arr]
    print("average num sentences: " + str(np.mean(post_lens)) + "\n")
    MINIMUM_POSTS = 36
    filtered_post_lens = list(filter(lambda x: x > MINIMUM_POSTS, post_lens))
    print("average num sentences for users > " + str(MINIMUM_POSTS) + " posts: " +
         str(np.mean(filtered_post_lens)) + "\n")

    # graph_all_post_lens(filtered_post_lens)

    all_post_lengths = [len(person['posts']) for person in people_arr]
    print("number of posts made by each person, sorted")
    print(sorted(all_post_lengths))

    all_forum_post_lengths = defaultdict(int)
    for person in people_arr:
        for post in person['posts']:
            all_forum_post_lengths[post['forum_name']] += 1

    print("\nall forums posted by number of posts")
    for forum_name in sorted(all_forum_post_lengths, key=lambda item:
    all_forum_post_lengths[item], reverse=True):
        print("{} {}".format(all_forum_post_lengths[forum_name], forum_name))

    print("\nall usernames sorted by number of posts > 100")
    sorted_people = sorted(people_json.items(),
        key=lambda item: len(item[1]['posts']), reverse=True)
    for person, obj in sorted_people:
        if len(obj['posts']) > 100:
            print(len(obj['posts']), person)

    # printing out all forum names (could look at posts/_finished/ folder also)
    # for easy access and to test other forums if necessary

    print("\nlist of all forum names")
    forum_names = set()
    for person in people_arr:
        unique_forums = np.unique([post['forum_name'] for post in person['posts']])
        for forum_name in unique_forums:
            forum_names.add(forum_name)
    print(forum_names)




    ### VISUALIZING POSTS

    # visualizing posts for ranger (only 5 sentences)
    # pca_visualize_posts('ranger', people_json)

    # visualizing posts for Helena1 (105 sentences)
    # pca_visualize_posts('Helena1', people_json)

    # visualizing posts for madmark (1590 sentences)
    # pca_visualize_posts('madmark', people_json)



    ### VISUALIZING A SPECIFIC FORUM

    # visualizing posts in mamistruggling forum
    # pca_visualize_forums('mamistruggling', people_json)

    # visualizing posts in pleasehelp forum
    # pca_visualize_forums('pleasehelp', people_json)

    pca_visualize_forums('solonely', people_json)



### HELPER FUNCTIONS BELOW

def graph_all_post_lens(post_lens):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.hist(post_lens)
    plt.show()

def pca_visualize_forums(forum_name, people_json):
    all_posts = []
    all_people = []
    all_sentiments_in_forum = []

    for person in people_json:
        for post in people_json[person]['posts']:
            if post['forum_name'] == forum_name:
               all_sentiments_in_forum.append(list(post['sentiments'].values()))
               all_posts.append(post)
            all_people.append(person)

    k = 1
    while True:
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(all_sentiments_in_forum)
        error = kmeans.inertia_
        if error / len(all_sentiments_in_forum) < 0.2:
            break
        k += 1

    cluster_centers = kmeans.cluster_centers_.tolist()
    labels = kmeans.labels_.tolist()

    points_to_pca = all_sentiments_in_forum + cluster_centers

    pca = PCA(n_components=2)
    values = pca.fit_transform(points_to_pca)

    # account for centroids also being in the mix. different unique category for them
    labels.extend([-1] * len(cluster_centers))
    all_posts.extend([{'text': "b'Centroid'"}] * len(cluster_centers))


    fig = plt.figure()
    ax = fig.add_subplot(111)
    x, y = [*values.T]
    ax.scatter(x, y, c=labels)

    plt.title("emotion values for " + forum_name)

    def onClick(sel):
        post_text = all_posts[sel.target.index]['text']
        if post_text == "b'Centroid":
            return sel.annotation.set_text(linewrap(post_text))

        person_name = all_people[sel.target.index]
        text = "user: {0}\n{1}".format(person_name, linewrap(post_text))
        return sel.annotation.set_text(text)

    mplcursors.cursor(ax).connect("add", lambda sel: onClick(sel))

    plt.title("Visualizing post emotions for forum: " + forum_name +
        "\nn: " + str(len(all_posts) - len(cluster_centers)))
    plt.show()

def pca_visualize_posts(person_name, people_json):
    person = people_json[person_name]

    post_objs = person['posts'].copy()
    sentiment_objs = [post['sentiments'] for post in post_objs]
    all_sentiments = [[item for item in sentiment.values()] for sentiment in sentiment_objs]
    centroids = person['centroids']
    labels = person['centroid_labels']

    # pca all the points at once to make sure everything is the same latent space
    all_points_to_pca = all_sentiments + centroids

    pca = PCA(n_components=2)
    values = pca.fit_transform(all_points_to_pca)

    # extend labels to account for centroids (all part of the same class)
    labels.extend([-1] * len(centroids))
    post_objs.extend([{'text': "b'Centroid'"}] * len(centroids))

    fig = plt.figure()

    ax = fig.add_subplot(111)
    x, y = [*values.T]
    ax.scatter(x, y, c=labels)

    def onClick(sel):
        text = post_objs[sel.target.index]['text']
        return sel.annotation.set_text(linewrap(text))

    mplcursors.cursor(ax).connect("add", lambda sel: onClick(sel))

    plt.title("Visualizing post emotions for person: " + person_name +
        "\nn: " + str(len(post_objs) - len(centroids)))
    plt.show()


# function to linewrap a piece of text using specified limit, for easier reading
# in visualizations.
def linewrap(text):
    # remove b' and ' from start and end of string
    text = text[2:-1]

    linewrap_limit = 30
    index = 0
    final_text = ""
    while index + linewrap_limit < len(text):
        subtext = text[index:index + linewrap_limit]
        index_last_space = subtext.rfind(' ')
        if index_last_space != -1:
            final_text += subtext[:index_last_space] + '\n' + subtext[index_last_space + 1:]
        else:
            final_text += subtext
        index += linewrap_limit
    final_text += text[index:]
    return final_text


if __name__ == "__main__":
    main()
