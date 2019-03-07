import json
import sys


def remove_zero_sentiments(data, threshold=0.6):
    filtered = {}

    for site,info in data.items():
        valid_posts = []
        for post in info['posts']:
            add = False
            for sentiment,val in post['sentiments'].items():
                if val > threshold:
                    add = True
                    break
            if add:
                valid_posts.append(post)
        if len(valid_posts) != 0:
            filtered[site] = info
            filtered[site]['posts'] = valid_posts

    return filtered



def main():
    file = 'news.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    new_data = remove_zero_sentiments(data)
    new_file = 'filtered_' + file

    with open(new_file, 'w') as outfile:
        json.dump(new_data, outfile)


if __name__ == "__main__":
    sys.exit(main())
