import requests
import json
import PyPDF2

URL = 'http://jisho.org/api/v1/search/words?keyword='

#Handled Errors
def make_req (keyword=''):
    try:
        response = requests.get(URL + keyword)
    except Exception:
        print("Seems like a network issue. Make sure you are connected to the"
              "internet!")
        return []

    data = json.loads(response.text)['data']
    return data

def get_most_relevant (keyword):
    data = make_req(keyword)
    if data == []:
        return "None found."
    else:
        res = ''
        try:
            res += (data[0]['japanese'][0]['word']) + '\n'
        except KeyError:
            pass
        res += (data[0]['japanese'][0]['reading'])
        return res

def get_relevant_data (data):
    if data == []:
        print(":( No meaning available. Either you aren't connected to the "
              "internet or you searched for an invalid word")
        return None
    result = []
    for word in data:
        word_data = []
        try:
            for key in word:
                if key in ('tags', 'attribution'):
                    continue
                if type(word[key]).__name__ == 'list':
                    word_data_data = []
                    for i in word[key]:
                        for keys in i:
                            if i[keys] != []:
                                word_data_data.append((keys, i[keys]))

                    word_data.append((key, word_data_data))
                else:
                    word_data.append((key, word[key]))
        except KeyError:
            pass
        result.append(word_data)
    return result