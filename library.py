import json
import os
import subprocess

import numpy as np
import pandas as pd


#get all filepaths from a directory, used to get names of node scripts to run
def get_file_paths(directory_path):
    file_paths = []

    if not os.path.exists(directory_path):
        return file_paths
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

#clean a directory !!!DANGEROUS!!!
def clean_path(path):
    # List all items in the directory
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        # Check if it's a file or directory
        if os.path.isfile(item_path):
            os.remove(item_path)  # Remove the file


def open_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return np.array(data)

#return a df with the best odds for each outcome and the provider
def find_best_odds(df):
    # Identify all the columns for team1 and team2 odds
    team1_cols = [col for col in df.columns if 'team1' in col]
    team2_cols = [col for col in df.columns if 'team2' in col]
    
    #find the maximum odds and their source, ignoring None values
    def max_with_source(lst, source_lst):
        max_value = None
        max_source = None
        for i, value in enumerate(lst):
            if value is not None and (max_value is None or value > max_value):
                max_value = value
                max_source = source_lst[i]
        return max_value, max_source

    # Apply the function to each row to find the best odds for team1 and team2
    df['best_team1_odds'], df['best_team1_source'] = zip(*df.apply(
        lambda row: max_with_source([row[col] for col in team1_cols], team1_cols), axis=1))
    df['best_team2_odds'], df['best_team2_source'] = zip(*df.apply(
        lambda row: max_with_source([row[col] for col in team2_cols], team2_cols), axis=1))
    
    cols_to_display = ['match', 'best_team1_odds', 'best_team1_source', 'best_team2_odds', 'best_team2_source']
    return df[cols_to_display]

# work out if the best odds present an arbitrage opportunity
def arbitrage(row):
    implied_team1 = 1 / float(row['best_team1_odds'])
    implied_team2 = 1 / float(row['best_team2_odds'])
    total = implied_team1 + implied_team2
    return round((1 - total)*100,2) if total < 1 else 0

# return unique match names, scraping procceess does not gaurentee returning the same events/matches
def get_names(data):
    names = []
    for d in data:
        match_names = [x['id'] for x in d]
        names.extend(match_names)
    names = list(map(lambda x: x.lower(), names))
    return np.unique(names)


def implied_odds(row):
    implied_team1 = 1 / float(row['best_team1_odds'])
    implied_team2 = 1 / float(row['best_team2_odds'])
    return implied_team1, implied_team2


#return bet sizes that are arbitrage oportunities and are whole number multiples of 5
#this is to avoid possible account suspension
#start at 5,5 then incement the value at the index of the smallest implied probability - Switch to incrementing the other
# when the ration of this value to the total is greater than the implied prob of likely outcome
def real_bets(implied_probs, odds, max_stake):
    # get the index of the min and max prob for the algo later on
    if implied_probs[0] > implied_probs[1]:
        max_index = 0
        min_index = 1
    else:
        max_index = 1
        min_index = 0

    stakes = [5,5]
    winning_stakes = []
    opp = False
    while(sum(stakes) < max_stake ):
        total = sum(stakes)
        payout_max = stakes[max_index] * odds[min_index]
        payout_min = stakes[min_index] * odds[max_index]

        #Arbitrage case so add to winning_stakes
        if payout_max >= total and payout_min >= total:
            opp = True
            winning_stakes.append(stakes.copy())

        #core of the algorithm
        if stakes[min_index] / total < implied_probs[max_index]:
            stakes[min_index] += 5
        else:
            stakes[max_index] += 5

    
    indices_to_remove = []
    #flip the inner arrays so they match up with odds order
    for i, s in enumerate(winning_stakes):
        #filter out the lower ones but make sure there is atleast 1
        if sum(winning_stakes[i]) < int(max_stake * 0.9) and len(winning_stakes) - len(indices_to_remove) > 5:
            indices_to_remove.append(i)
        else:
            winning_stakes[i] = s[::-1]
    
    filtered_list = [item for idx, item in enumerate(winning_stakes) if idx not in indices_to_remove]

    return filtered_list

#from the various json files return a df containing only arbitrage opportunities
def get_arbs(event):
    bookie_names = []
    #data is an array of json loaded from each file
    data = []
    filepaths = get_file_paths(f'data/{event}')

    for path in filepaths:
        data.append(open_data(path))
        bookie_names.append(path.split('/')[-1].split('.')[0])
        
    match_names = get_names(data)

    df = pd.DataFrame({'match': match_names})

    for d, name in zip(data, bookie_names):
        team1_dict = {x['id'].lower(): x['odds'][0] for x in d if len(x['odds']) > 2}
        team2_dict = {x['id'].lower(): x['odds'][2] for x in d if len(x['odds']) > 2}

        team1 = [team1_dict.get(match) for match in match_names]
        team2 = [team2_dict.get(match) for match in match_names]

        df[f'{name}_team1'] = team1
        df[f'{name}_team2'] = team2 

    best_odds = find_best_odds(df).copy()
    best_odds.dropna(inplace=True)
    best_odds['%_profit'] = best_odds.apply(lambda row: arbitrage(row), axis=1)
    
    mask = best_odds['%_profit'] != 0
    best_odds = best_odds[mask]
    best_odds[['team1_implied_odds', 'team2_implied_odds']] = best_odds.apply(lambda row: implied_odds(row), axis=1, result_type='expand')

    best_odds['best_team1_odds'] = best_odds['best_team1_odds'].astype(float)
    best_odds['best_team2_odds'] = best_odds['best_team2_odds'].astype(float)

    return best_odds.sort_values(by='%_profit', ascending=False)
