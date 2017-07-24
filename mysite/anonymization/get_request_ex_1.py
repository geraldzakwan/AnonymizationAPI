# Reference:
# https://github.com/google/google-api-python-client/blob/master/samples/customsearch/main.py

import sys
from apiclient.discovery import build

api_key = 'AIzaSyDkSCA8agvst49gtKEjrxRnI57lCqV9vBM'
cx_key = '013692161269702497108:vgnkfyixhmo'

def get_total_results(word):
    service = build("customsearch", "v1", developerKey=api_key)

    res = service.cse().list(q=word, cx=cx_key,).execute()

    total_results = float(res['queries']['request'][0]['totalResults'])

    return total_results

def co_occurence(word1, word2):
    and_total_results = get_total_results(word1 + " AND " + word2)
    or_total_results = get_total_results(word1 + " OR " + word2)

    return and_total_results/or_total_results

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        sys.exit('Supply first word and second word')
    print(co_occurence(sys.argv[1], sys.argv[2]))
