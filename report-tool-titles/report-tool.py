# Basic report generator for titles in InsightIDR - Kellvin Romano / byth22

## libs necessárias
import requests
import json
import re
from datetime import date
from collections import Counter
import sys


## func para levantar títulos de investigações e separa-los entre custom alerts e alertas nativos
def check_titles(data):
    titles = []
    for i in data['data']:
    ## try-execpt para dicernir entre titulos de custom alerts e titulos de alertas nativos
        try:
            #titles.append(i['alerts'][0]['type_description'])
            #print (i['alerts'])
            if 'logs' in str(i):
                titles.append(i['title'])

            else:
                titles.append(i['alerts'][0]['type_description'])
        except:
            pass

    count_dict = dict(Counter(titles).items())

    return (count_dict)


## func para puxar de investigações via api REST
def data_receive():
    today = date.today()
    url = 'https://<seu_país_cloud>.api.insight.rapid7.com/idr/v1/investigations' # <- é necessário setar o endpoint do seu país

    headers = {
        'X-Api-Key': '', # <- é necessario setar sua api key
    }

    params = {
        #'start_time' : str(today)+'T00:00:00Z',
        'start_time' : '2022-06-20'+'T00:00:00Z', # <- é necessário setar a data inicial de pesquisa
        'size' : '1000',
    }

    r = requests.get(url, headers=headers, params=params)
    data = json.loads(r.content)

    return data


## func para printar lista em melhor visualização
def print_list(titles):
    for key, value in titles.items():
        print(key, ' : ', value)

    return 0


def main():
    data = data_receive()
    titles = check_titles(data)
    print_list(titles)
    #print (titles)


main()
