## Script de watch dogs para reestabelecer events sources em estado de Warning
## Kellvin Romano - byth22

import requests
import json
import re
#from selenium import webdriver
from seleniumwire import webdriver
import re
import time
import unicodedata
import pickle
import ast
import sys
import os

# Selenium in background - https://stackoverflow.com/questions/5370762/how-to-hide-firefox-window-selenium-webdriver
os.environ['MOZ_HEADLESS'] = '1'

def get_cookie():
    ## Conexão por meio do geckodriver para pegar o cookie
    driver = webdriver.Firefox(executable_path=r'.\geckodriver.exe')
    driver.get('https://insight.rapid7.com/login')

    time.sleep(3)
    username=driver.find_element_by_id("okta-signin-username");
    password=driver.find_element_by_id("okta-signin-password");


    username.send_keys("");    # usuario
    password.send_keys("");    # senha
    driver.find_element_by_id("okta-signin-submit").click()

    time.sleep(15)
    expectedUrl= driver.current_url;
    #print expectedUrl.rsplit('/', 1)[-1]

    #print driver.execute_script("var req = new XMLHttpRequest();req.open('GET', document.location, false);req.send(null);return req.get(headerName)")
    #print driver.execute_script("return navigator.userAgent")
    for request in driver.requests:
        #print (request.headers) # <----------- Request headers
        if (re.search('x-csrf-token:(.*)',str(request.headers))):
            match = re.search('x-csrf-token:(.*)',str(request.headers))
            break
            
    cookie = driver.get_cookies()[5]['value']
    driver.close()
    driver.quit()
    print ("[+] Cookies gerados!")
    return cookie, match.group(1)


def ids_list(cookie):
    global pToken
    requests.packages.urllib3.disable_warnings()
    cookies = {
    'IPIMS_SESSION': cookie}
    #print cookies


    headers = {
        'Host': 'razor.insight.rapid7.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'X-Orgproduct-Token': pToken,
        'R7-Organization-Product-Token': pToken,
        'Origin': 'https://us.idr.insight.rapid7.com',
        'Dnt': '1',
        'Referer': 'https://us.idr.insight.rapid7.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Te': 'trailers',
        'Connection': 'close',
    }

    #params = (
     #   ('status', 'WARNING'),
    #)

    #r3 = requests.get('https://razor.insight.rapid7.com/api/1/eventsource/filters', headers=headers, cookies=cookies, params=params, verify=False)

    params = (
    ('index', '0'),
    ('size', '20'),
    ('status', 'WARNING'),
    ('name', ''),
)

    r = requests.get('https://razor.insight.rapid7.com/api/2/eventsource', headers=headers, params=params, cookies=cookies, verify=False)
    data = json.dumps(str(r.content))
    data1 = ast.literal_eval(data)
    ids_events = re.findall(r'\[\{\"id\":\"(.*?)\",\"name', data1)
    ids_events1 = re.findall(r',\{"id\":\"(.*?)\",\"name', data1)

    for i in ids_events1:
        ids_events.append(i)

    print ("[+] Lista de fontes de eventos em estado WARNING obtidos!")
    return ids_events


def pause_sources(lista, cookies, csrf):
    global pToken
    requests.packages.urllib3.disable_warnings()
    cookies = {
    'IPIMS_SESSION': cookies}
    #print cookies


    headers = {
        'Host': 'razor.insight.rapid7.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'X-Csrf-Token': csrf.strip(),
        'Csrftoken': csrf.strip(),
        'X-Orgproduct-Token': pToken,
        'R7-Organization-Product-Token': pToken,
        'Origin': 'https://us.idr.insight.rapid7.com',
        'Dnt': '1',
        'Referer': 'https://us.idr.insight.rapid7.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Te': 'trailers',
        'Connection': 'close',
        }

    #print (headers)
    #print (lista)
    for i in lista:
        #print (i)
        response = requests.put('https://razor.insight.rapid7.com/api/1/eventsource/'+i+'/stop', headers=headers, cookies=cookies, verify=False)
        #print (response.status_code)
        #print (response.content)
        print ("[+] Event source %s stopped!" % i)
        #sys.exit()
        
    return 0


def ids_list_paused(cookies):
    global pToken
    requests.packages.urllib3.disable_warnings()

    cookies = {
        'IPIMS_SESSION': cookies,
    }

    headers = {
        'Host': 'razor.insight.rapid7.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        #'X-Csrf-Token':csrf,
        #'Csrftoken':csrf,
        'X-Orgproduct-Token': pToken,
        'R7-Organization-Product-Token': pToken,
        'Origin': 'https://us.idr.insight.rapid7.com',
        'Referer': 'https://us.idr.insight.rapid7.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Te': 'trailers',
        'Connection': 'close',
    }
    
    params = (
        ('index', '0'),
        ('size', '20'),
        ('status', 'STOPPED'),
        ('name', ''),
    )

    r = requests.get('https://razor.insight.rapid7.com/api/2/eventsource', headers=headers, params=params, cookies=cookies, verify=False)
    data = json.dumps(str(r.content))
    data1 = ast.literal_eval(data)
    ids_events = re.findall(r'\[\{\"id\":\"(.*?)\",\"name', data1)
    ids_events1 = re.findall(r',\{"id\":\"(.*?)\",\"name', data1)

    for i in ids_events1:
        ids_events.append(i)

    print ("[+] Lista de fontes de eventos pausados obtidos!")
    return ids_events


def resume(lista, cookies, csrf):
    global pToken
    import requests

    cookies = {
        'IPIMS_SESSION': cookies,
    }

    headers = {
        'Host': 'razor.insight.rapid7.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'X-Csrf-Token': csrf.strip(),
        'Csrftoken': csrf.strip(),
        'X-Orgproduct-Token': pToken,
        'R7-Organization-Product-Token': pToken,
        'Origin': 'https://us.idr.insight.rapid7.com',
        'Referer': 'https://us.idr.insight.rapid7.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Content-Length': '0',
        'Te': 'trailers',
        'Connection': 'close',
    }

    for i in lista:
        #print (i)
        response = requests.put('https://razor.insight.rapid7.com/api/1/eventsource/'+i+'/start', headers=headers, cookies=cookies, verify=False)
        #print (response.status_code)
        #print (response.content)
        print ("[+] Event source %s resumed!" % i)
        #sys.exit()
        
    return 0


def main():
    cookies = ''
    csrf = ''
    global pToken
    pToken = '' # <- necessario alterar para o token do seu IDR
        
    while True:   
        if bool(cookies):
            ids_to_pause = ids_list(cookies)
            pause_sources(ids_to_pause, cookies, csrf)
            #time.sleep(120)
            ids_paused = ids_list_paused(cookies)
            resume(ids_paused, cookies, csrf)
            time.sleep(2)

        else:
            cookies, csrf = get_cookie()
            ids_to_pause = ids_list(cookies)
            pause_sources(ids_to_pause, cookies, csrf)
            #time.sleep(120)
            ids_paused = ids_list_paused(cookies)
            resume(ids_paused, cookies, csrf)
            time.sleep(2)
    
main()
