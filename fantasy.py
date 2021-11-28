import requests, json, time, os
import pandas as pd

scoring = {'kills': 0.3,
           'deaths': - 0.3,
           'last_hits': 0.003,
           'denies': 0.003,
           'gold_per_min': 0.002,
           'tower_kills': 1,
           'roshan_kills': 1,
           'obs_placed': 0.5,
           'camps_stacked': 0.5,
           'rune_pickups': 0.25,
           'stuns': 0.05}

# fails if replay not parsed
def find_first_blood(data):
    first_kill = [p['kills_log'][:1] for p in data['players']]
    t = data['first_blood_time'] + 1
    p = None
    for player, kill in enumerate(first_kill):
        if kill:
            kill_t = kill[0]['time']
            if kill_t <= t:
                t = kill_t
                p = player
    return p

# not confident about this one
def get_teamfight_perc(data):
    part = [0 for i in range(10)]
    for fight in data['teamfights']:
        for i, p in enumerate(fight['players']):
            if p['damage'] != 0:
                part[i] += 1
    N = len(data['teamfights'])
    if N == 0: N = 1 # division by 0
    part = [p / N for p in part]
    return part


match_list = pd.read_csv('match_list.csv', index_col = 0)

# points collected in match_list
scores = []

for team_id, matches in match_list.items():
    team_id = int(team_id)
    for match_id in matches:
        m_id = str(match_id)

        path = os.path.join('match_data', m_id + '_data.json')
        if not os.path.isfile(path):
            continue

        file = open(path, 'r')
        data = json.load(file)
        file.close()

        # radiant or dire
        side = None
        if data['radiant_team']['team_id'] == team_id:
            side = True
        if data['dire_team']['team_id'] == team_id:
            side = False

        # keep track of players on team
        players = {k: 0 for k, p in enumerate(data['players'])
                   if p['isRadiant'] == side}

        # check first blood
        try:
            fb = find_first_blood(data)
        except TypeError:
            # happens when replay is not parsed
            continue
            
        if fb != None and fb in players:
            players[fb] += 4.0

        # check fighting percentage
        part = get_teamfight_perc(data)
        for p in players:
            players[p] += 3.0 * part[p]

        # the rest of the scoring criterias
        for p in players:
            for c, pt in scoring.items():
                players[p] += pt * data['players'][p][c]

        # add by player id
        for p, s in players.items():
            account_id = data['players'][p]['account_id']
            scores += [[account_id, team_id, match_id, s]]

# results
scores = pd.DataFrame(scores, columns = ['account_id', 'team_id', 'match_id', 'score'])
scores.to_csv('scores.csv')

# best median points
fantasy = scores.groupby('account_id')[['team_id', 'score']].median()
fantasy = pd.DataFrame(fantasy).sort_values('score', ascending = False)

id2names = pd.read_csv('id2name.csv', encoding = 'utf-16', index_col = 0)
names = []
for i in fantasy.index:
    if i in id2names.index:
        n = id2names.loc[i]['name']
    else:
        n = requests.get("https://api.opendota.com/api/players/" + str(i)).json()['profile']['name']
        print('MISSING', i, n)
        time.sleep(1)
    names += [n]
    print(n, fantasy.loc[i]['score'])
fantasy['name'] = names

fantasy.to_csv('fantasy.csv')
