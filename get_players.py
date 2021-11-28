import pandas as pd
import numpy as np

from utilities import *

# get players and their IDs
data = pd.read_csv('DPC_schedule.csv', dtype = object, index_col = 0)

teams = np.append(data[['team_1', 'id_1']], data[['team_2', 'id_2']], axis = 0)
teams = list({tuple(t) for t in teams})
pros = OD_get_pro_ids()

# not great, opendota doesn't have all this data yet
# team_players = {t: get_team_players(t) for t in teams}
# once a few weeks of DPC have gone by, this should be the way

players = []
for t, tid in teams:
    names = D2_get_team_player_names(tid)
    for n in names:
        if n not in pros:
            # debug messages for missing players, fix manually
            # TODO: some regex, partial match, other sources, etc..
            print(n, 'missing', end = '')
            id2 = D2_get_player_id(n)
            if id2:
                n2 = OD_get_player_name(id2)
                print(', found', id2, 'with name', n2, end = '')
            print()
        else:
            players += [[t, tid, n, pros[n]]]

players = pd.DataFrame(players, columns = ['team', 'team_id', 'name', 'player_id'])
players.to_csv('players.csv')
