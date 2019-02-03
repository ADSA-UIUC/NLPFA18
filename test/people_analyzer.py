import json
import numpy as np

def main():
    with open('../data/processed/people.json', 'r') as f:
        people_json = json.load(f)

    # could have formatted this better in the first place, but each person 
    # is a different property in the json file for now. so turn back into
    # array for easy access
    people_arr = [people_json[person] for person in people_json]

    average = np.mean([len(person['posts']) for person in people_arr])
    print("average num sentences: " + str(average))

if __name__ == "__main__":
    main()