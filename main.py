
import numpy as np
import pandas as pd

from library import *

TAB_file = 'data/rugby_union/TAB.json'
sportsbet_file = 'data/rugby_union/sportsbet.json'

TAB_data = open_data(TAB_file)
sportsbet_data = open_data(sportsbet_file)

match_names = np.concatenate(([x['id'] for x in TAB_data], [x['id'] for x in sportsbet_data]))
match_names = np.unique(match_names)

df = pd.DataFrame({'match': match_names})

TAB_team1_dict = {obj['id']: obj['odds'][0] for obj in TAB_data}
TAB_team2_dict = {obj['id']: obj['odds'][2] for obj in TAB_data}
sportsbet_team1_dict = {obj['id']: obj['odds'][0] for obj in sportsbet_data}
sportsbet_team2_dict = {obj['id']: obj['odds'][2] for obj in sportsbet_data}


TAB_team1 = [TAB_team1_dict.get(match) for match in match_names]
TAB_team2 = [TAB_team2_dict.get(match) for match in match_names]
sportsbet_team1 = [sportsbet_team1_dict.get(match) for match in match_names]
sportsbet_team2 = [sportsbet_team2_dict.get(match) for match in match_names]

df['TAB_team1'] = TAB_team1
df['TAB_team2'] = TAB_team2
df['sportsbet_team1'] = sportsbet_team1
df['sportsbet_team2'] = sportsbet_team2

best_odds = find_best_odds(df).copy()
best_odds['arbitrage'] = best_odds.apply(lambda row: arbitrage(row), axis=1)
mask = best_odds['arbitrage'] == 1
print(best_odds[mask])
``
