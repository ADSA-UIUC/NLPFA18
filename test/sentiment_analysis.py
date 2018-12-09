from apikey import api 
from watson_developer_cloud import ToneAnalyzerV3, WatsonApiException
import csv, os, sys, re
import pandas as pd

# version can be 2016-05-19 or 2017-09-21
# 2016 version returns between 0 and 1, 2017 returns between 0.5 and 1
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    username=api['ToneAnalyzer']['username'],
    password=api['ToneAnalyzer']['password'],
    url=api['ToneAnalyzer']['URL']
)

def analyze_tones(text):
    try:
        result = tone_analyzer.tone(
            {'text': text},
            'application/json'
        ).get_result()
        return result
    except WatsonApiException as ex:
        error_msg = "Method failed with status code " + str(ex.code) + ": " + ex.message
        throw Exception(error_msg)

def to_tone_dict(tone_arr_json):
    """
    turn [dict({'score': {float}, 'tone_id': {str}, 'tone_name', {str}})] * {1 <= int <= 6}
    into [{float}] * 7 where each index is the score of the tone specified in id_to_key
    """
    tone_dict = {'Anger': 0, 'Fear': 0, 'Joy': 0, 'Sadness': 0, 'Analytical': 0, 'Confident': 0, 'Tentative': 0}
    for tone in tone_arr_json:
        tone_dict[tone['tone_name']] = tone['score']
    
    return tone_dict

#read in data from data folder
def analyze_posts(input_filepath):
    # analyze data in folder, return analysis into csv
    sentiments_doclevel = {'post #': [], 'username': [], 'text': [], 'Anger': [], 'Fear': [], 'Joy': [], 'Sadness': [], 'Analytical': [], 'Confident': [], 'Tentative': []}
    sentiments_sentencelevel = {'post #': [], 'username': [], 'text': [], 'Anger': [], 'Fear': [], 'Joy': [], 'Sadness': [], 'Analytical': [], 'Confident': [], 'Tentative': []}

    csv = pd.read_csv(input_filepath)
    total_len = len(csv)
    for ind, row in enumerate(csv.iterrows()):
        if ((ind + 1) / total_len * 100) % 5 < 0.1:
            print('{.1}% done'.format(ind / total_len * 100))
        result = analyze_tones(row[1]['post content'])

        # document level tones 
        sentiments_doclevel['post #'].append(row[1][0])
        sentiments_doclevel['username'].append(row[1]['username'])
        sentiments_doclevel['text'].append(row[1]['post content'])
        doclevel_tones = to_tone_dict(result['document_tone']['tones'])
        for tone in doclevel_tones.keys():
            sentiments_doclevel[tone].append(doclevel_tones[tone])

        # if only one sentence- only doc tones, no sentence tone
        if 'sentences_tone' in result:
            # sentence level tones
            for sentence in result['sentences_tone']:
                sentiments_sentencelevel['post #'].append(row[1][0])
                sentiments_sentencelevel['username'].append(row[1]['username'])
                sentiments_sentencelevel['text'].append(sentence['text'])
                sentencelevel_tones = to_tone_dict(sentence['tones'])
                for tone in sentencelevel_tones.keys():
                    sentiments_sentencelevel[tone].append(sentencelevel_tones[tone])
    return pd.DataFrame(sentiments_doclevel), pd.DataFrame(sentiments_sentencelevel)

def main():
    # take output and put into raw data output folder
    path = "../data/raw/posts/_toprocess/"
    input_files = os.listdir(path) 
    for filename in input_files:
        if not re.match(".+[0-9]+\.csv", filename):
            continue
        print('starting with ' + filename)
        doclevel, sentencelevel = analyze_posts(path + filename)
        doclevel.to_csv('../data/raw/sentiments/' + filename[:-4] + '_doclevelsentiments.csv', index=False)
        sentencelevel.to_csv('../data/raw/sentiments/' + filename[:-4] + '_sentencelevelsentiments.csv', index=False)
        os.system("mv {} ../data/raw/posts/_finished/".format(filename))
        print('finished with ' + filename)

if __name__ == "__main__":
    sys.exit(main())
