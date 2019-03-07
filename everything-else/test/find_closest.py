# finding closest people to input person
# plot everyone as single points, find closest in terms of:
#   centroid distance
#   average mood(?)
#   keywords from text

import json
from sentiment_analysis import analyze_tones, to_tone_dict

class FindClosest:
    def __init__(self, people_json):
        with open(people_json) as f:
            self._data = json.load(f)
        print("loading Word2Vec model...")
        start_time = time.time()
        self._model = gensim.models.KeyedVectors.load_word2vec_format('../data/GoogleNews-vectors-negative300.bin', binary=True)
        print("finished loading model! took: {} seconds".format(time.time() - start_time))

    def input(self, input_str):
        if input_str in self._data:
            # input is a username
            input_person = self._data[input_str]
            self._result = {person: _distance_people(self._data[person], input_person) for person in self._data} 
        else:
            self._result = {person: _distance_person_text(self._data[person], input_str) for person in self._data}


    def _distance_sentiments(sentiments_own, sentiments_other):
        # post_centroids is in a list bc some people may have more than 1 centroid that
        # describes their posts
        return max(_sentiment_distance(sentiment, sentiments_other) for sentiment in sentiments_own)       

    def _distance_all_moods(self, mood_list1, mood_list2):
        # multithreaded work might be useful here
        # find all combinations of mood_list1 and mood_list2 and average the mood distance
        # mood_distance defined by distance between words via Google Word2Vec
        sum = 0
        count = 0
        for mood1 in mood_list1:
            for mood2 in mood_list2:
                if mood1 == "None" | mood2 == "None":
                    continue
                count += 1
                try:
                    sum += _distance_two_words(mood1, mood2)
                except KeyError as e:
                    # KeyError means Word2Vec didn't have the word in the vocabulary
                    print("Error: {}".format(e.message))
                    count -= 1
        if count == 0:
            return 0
        return sum / count

    def _distance_two_words(self, word1, word2):
        # words in Google Word2Vec have underscores rather than spaces
        word1_edited = word1.replace(" ", "_")
        word2_edited = word2.replace(" ", "_")
        return self._model.wv.similarity(w1=word1_edited, w2=word2_edited)

    def _distance_person_text(self, person_own, text_other):
        # centroid distance is the only metric
        try:
            sentiments_other = to_tone_dict(analyze_tones(text_other)['document_tone']['tones'])
        except Exception as e:
            throw e
        centroid_distance = _distance_sentiments(person_own['post_centroids'], sentiments_other)

        return centroid_distance

    def _distance_people(self, person_own, person_other):
        # weighted average of centroid distance, average mood similarity, (keywords)
        centroid_distance = _distance_sentiments(person_own['post_centroids'], person_other['post_centroids'])
        person_own_moods = [post['mood'] for post in person_own['posts']]
        person_other_moods = [post['mood'] for post in person_other['posts']]
        average_mood_distance = _distance_all_moods(person_own_moods, person_other_moods)
        
        return centroid_distance + average_mood_distance 


 
    def get_closest_sorted(self):
        # return answer in sorted order, by distance
        return sorted(self._result.iteritems(), key=itemgetter(1), reverse=True)

def main(input):
    find_closest = FindClosest("../data/processed/people.json")
    find_closest.input(input)
    print(find_closest.get_closest_sorted()[:10])

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
