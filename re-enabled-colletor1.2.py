# re-enabled colletor - Kellvin Romano

import requests
import json
import re
from datetime import date


def check_accountsIds(data):
    cont = 1
    ids = []
    for i in data['data']:
        #if "Account Enabled" in i['alerts'][0]['type']:
        #   print (i)
        #if "OPEN" in i['status'] and not "assignee" in i.keys():
        if "OPEN" in i['status'] and "re-enabled" in i['title']:
        #if "re-enabled" in i['title']:
                #print (i)
                print ("    "+re.sub(r're-enabled by', 'reabilitada pelo ldap admin', re.sub(r'Account', 'Conta', i['title']+";")))
                ids.append(i['id'])

        cont+=1

    #print ("")
    print ("    Poderiam verificar se a atividade é legítima e nos encaminhar o respectivo ticket? Obrigado desde já.")
    #print ("")
    print ("Att,")
    print ("[!} --------------------------------------------------------------------------------")
    return ids

def data_receive():
    today = date.today()
    url = 'https://us2.api.insight.rapid7.com/idr/v1/investigations' # <- é necessário setar o endpoint do seu país

    headers = {
        'X-Api-Key': '', # <- é necessário setar sua api key
    }

    params = {
        'start_time' : str(today)+'T00:00:00Z',
    }

    r = requests.get(url, headers=headers, params=params)
    data = json.loads(r.content)

    return data

def change_toInvestigate(ids):
    print ("[+] Alterando status para \"investigating\"!")
    for i in ids:
        url = 'https://us2.api.insight.rapid7.com/idr/v1/investigations/'+i+'/status/investigating' # <- é necessário setar o endpoint do seu país

        headers = {
            'X-Api-Key': '', # <- é necessário setar sua api key
        }

        r = requests.put(url, headers=headers)


def main():
    data = data_receive()
    ids = check_accountsIds(data)
    change_toInvestigate(ids)
main()
