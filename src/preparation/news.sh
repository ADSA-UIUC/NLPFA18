source /Users/shawkagawa/Documents/UIUC/FA18/ADSA/ADSA_NLP_Healthcare_Project/NLPFA18/src/preparation/env/bin/activate
pip install -r requirements.txt
python3 /Users/shawkagawa/Documents/UIUC/FA18/ADSA/ADSA_NLP_Healthcare_Project/NLPFA18/src/preparation/get_newsAPI_headlines.py
python3 /Users/shawkagawa/Documents/UIUC/FA18/ADSA/ADSA_NLP_Healthcare_Project/NLPFA18/src/preparation/sentiment_analysis_news.py
python3 /Users/shawkagawa/Documents/UIUC/FA18/ADSA/ADSA_NLP_Healthcare_Project/NLPFA18/src/preparation/split_people_scikit.py
touch ~/Desktop/successfulAPICall
deactivate
