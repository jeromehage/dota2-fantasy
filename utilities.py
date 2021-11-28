import requests, json, os.path

# opendota
def OD_get_team_matches(team_id, limit = None):
    request = requests.get('https://api.opendota.com/api/teams/{}/matches'.format(team_id))
    return [m['match_id'] for m in request.json()[:limit]]

def OD_get_team_players(team_id):
    request = requests.get('https://api.opendota.com/api/teams/{}/players'.format(team_id))
    return {p['account_id']: p['name'] for p in request.json() if p['is_current_team_member']}

def OD_get_pro_ids():
    res = requests.get('https://api.opendota.com/api/proPlayers/').json()
    return {r['name']: r['account_id'] for r in res}

def OD_get_pro_matches(less_than_match_id = None):
    # limited to 100 matches
    if less_than_match_id:
        url = 'https://api.opendota.com/api/proMatches/?less_than_match_id={}'.format(less_than_match_id)
    else:
        url = 'https://api.opendota.com/api/proMatches/'
    return requests.get(url).json()

def OD_get_player_name(player_id):
    res = requests.get('https://api.opendota.com/api/players/{}'.format(player_id)).json()
    if res['profile']['name']:
        return res['profile']['name']
    else:
        return res['profile']['personaname']

def OD_get_match_by_id(match_id):
    m_id = str(match_id)
    path = os.path.join('match_data', m_id + '_data.json')
    if not os.path.isfile(path):
        # fetch match data
        request = requests.get("https://api.opendota.com/api/matches/" + m_id)
        if request.ok:
            print("GET:", m_id)
            data = request.json()
            # save it
            file = open(path, 'w')
            json.dump(data, file)
            file.close()
            return True
    return False

# dota2.com
def D2_get_team_player_names(team_id):    
    url = 'https://www.dota2.com/majorsregistration/teammembers?team_id={}'
    res = requests.get(url.format(team_id)).json()
    return {r['nickname']: r['full_name'] for r in res}

def D2_get_player_id(name):
    # note: not great, try searching Miracle ..
    url = 'https://www.dota2.com/majorsregistration/playerlist?substr={}'
    res = requests.get(url.format(name)).json()
    for r in res:
        l = r['label']
        n = l[l.index('(') + 1: l.index(')')]
        if n.strip().lower() == name.lower():
            return r['value']
    return None

def D2_get_team_id(name):
    url = 'https://www.dota2.com/majorsregistration/teamlist?substr='
    req = requests.get(url + name.replace(' ', '%20')) # or urllib quote
    if req.ok:
        res = req.json()
        if res:
            for r in res:
                if r['team_name'].strip().lower() == name.lower():
                    return r['team_id']

        else:
            # try searching for keywords if no match found
            words = name.split()
            if len(words) > 1:
                # print('searching for', words[0], 'instead of', name)
                res = requests.get(url + words[0]).json()
                if res:
                    for r in res:
                        if all([n1.lower() == n2.lower() for n1, n2
                                in zip(r['team_name'].split(), words)]):
                            return r['team_id']
    return ''
