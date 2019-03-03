from apikey import keys
from watson_developer_cloud import ToneAnalyzerV3, WatsonApiException
import csv, os, sys, re
import pandas as pd

# version can be 2016-05-19 or 2017-09-21
# 2016 version returns between 0 and 1, 2017 returns between 0.5 and 1
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    username=keys['ToneAnalyzer']['username'],
    password=keys['ToneAnalyzer']['password'],
    url=keys['ToneAnalyzer']['URL']
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
        raise Exception(error_msg)

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
    sentiments_doclevel = {'username': [], 'text': [], 'Anger': [], 'Fear': [], 'Joy': [], 'Sadness': [], 'Analytical': [], 'Confident': [], 'Tentative': []}
    sentiments_sentencelevel = {'username': [], 'text': [], 'Anger': [], 'Fear': [], 'Joy': [], 'Sadness': [], 'Analytical': [], 'Confident': [], 'Tentative': []}

    csv = pd.read_csv(input_filepath, engine='c')
    total_len = len(csv)

    for ind, row in enumerate(csv.iterrows()):
        print_progress(ind, total_len)

        result = analyze_tones(row[1]['title'])

        # document level tones
        sentiments_doclevel['username'].append(row[1]['source'])
        sentiments_doclevel['text'].append(row[1]['title'])
        doclevel_tones = to_tone_dict(result['document_tone']['tones'])
        for tone in doclevel_tones.keys():
            sentiments_doclevel[tone].append(doclevel_tones[tone])

        # if only one sentence- only doc tones, no sentence tone
        if 'sentences_tone' in result:
            # sentence level tones
            for sentence in result['sentences_tone']:
                sentiments_sentencelevel['username'].append(row[1]['source'])
                sentiments_sentencelevel['text'].append(sentence['text'])
                sentencelevel_tones = to_tone_dict(sentence['tones'])
                for tone in sentencelevel_tones.keys():
                    sentiments_sentencelevel[tone].append(sentencelevel_tones[tone])
    return pd.DataFrame(sentiments_doclevel), pd.DataFrame(sentiments_sentencelevel)


def print_progress(current_index, total_len, every_n_percent=5, epsilon=0.1):
    """
    prints the current progress (in percent) given the current index and the total
    """
    if ((current_index + 1) / total_len * 100) % every_n_percent < epsilon:
        print('{0:.3}% done'.format(current_index / total_len * 100))


def main():
    # take output and put into raw data output folder
    path = "sentiments/"
    input_files = os.listdir(path + "_todo/")
    for filename in input_files:
        if filename.startswith("."): continue

        print('starting with ' + filename)
        doclevel, _ = analyze_posts(path + "_todo/" + filename)
        if filename[:-4] + '_doclevelsentiments.csv' in os.listdir(path):
            with open(path + filename[:-4] + '_doclevelsentiments.csv', 'a') as f:
                writer = csv.writer(f)
                for row in doclevel.values:
                    writer.writerow(row[1:])
            print('appended to {}'.format(path + filename[:-4] + '_doclevelsentiments.csv'))
        else:
            doclevel.to_csv(path + filename[:-4] + '_doclevelsentiments.csv', index=False,
            index_label=False)
        os.system("mv {} {}".format(path + "_todo/" + filename, path + "_finished/" + filename[:-4] +
                str(int(len(os.listdir(path + "_finished/")) / 7)) + ".csv"))
        print('finished with ' + filename)

if __name__ == "__main__":
    sys.exit(main())
