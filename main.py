
import numpy as np
import pandas as pd

from library import *


def get_arbs():
    bookie_names = []
    #data is an array of json loaded from each file
    data = []
    filepaths = get_file_paths('data/rugby_union')

    for path in filepaths:
        data.append(open_data(path))
        bookie_names.append(path.split('/')[-1].split('.')[0])
        
    match_names = get_names(data)

    df = pd.DataFrame({'match': match_names})

    for d, name in zip(data, bookie_names):
        team1_dict = {x['id']: x['odds'][0] for x in d}
        team2_dict = {x['id']: x['odds'][2] for x in d}

        team1 = [team1_dict.get(match) for match in match_names]
        team2 = [team2_dict.get(match) for match in match_names]

        df[f'{name}_team1'] = team1
        df[f'{name}_team2'] = team2 

    best_odds = find_best_odds(df).copy()
    best_odds['%_profit'] = best_odds.apply(lambda row: arbitrage(row), axis=1)
    
    mask = best_odds['%_profit'] != 0
    best_odds = best_odds[mask]
    # best_odds[['team1_implied_odds', 'team2_implied_odds']] = best_odds.apply(lambda row: implied_odds(row), axis=1, result_type='expand')
    return best_odds

print(get_arbs())

