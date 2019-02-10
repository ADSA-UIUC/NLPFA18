import json, sys
from pprint import pprint

class PeopleFinder:
    def __init__(self, people_file):
        with open(people_file, 'r') as f:
            for row in f:
                text = row

        people = json.loads(text)

        threshold = 10
        people_cut = [people[person] for person in people if len(people[person]['posts']) > threshold]
        
        for name in people:
            person = people[name]
            posts = person['posts']
            centroids = person['centroids']

        



def main():
    PeopleFinder('../data/processed/people.json')

if __name__ == "__main__":
    sys.exit(main())