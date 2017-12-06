#!/usr/bin/python3
import requests


# Define function for making API requests
def xmlstats(
        endpoint,
        form='.json',
        sport=None,
        date=None,
        event=None,
        category=None
        ):

    token = YOUR_XMLSTATS_TOKEN
    authorization = 'Bearer ' + token
    agent = [YOUR_AGENT_NAME]
    headers = {'Authorization': authorization, 'User-Agent': agent}

    requrl = 'https://erikberg.com/'
    payload = {}
    if endpoint == 'events':
        requrl += endpoint + form
        if sport is not None:
            payload.update({'sport': sport})
        if date is not None:
            payload.update({'date': date})

    elif endpoint == 'boxscore':
        requrl += sport + '/' + endpoint + '/' + event + form

    elif endpoint == 'standings':
        requrl += sport + '/' + endpoint
        if date is not None:
            requrl += '/' + date + form
        else:
            requrl += form

    elif endpoint == 'leaders':
        requrl += sport + '/' + endpoint + '/' + category + form

    elif endpoint == 'daily-leaders':
        requrl += sport + '/' + endpoint
        if date is not None:
            requrl += '/' + date
        requrl += form

    else:
        print('That\'s not a valid endpoint.')
        exit()

    r = requests.request('GET', requrl, params=payload, headers=headers)
    r = r.json()

    return r
