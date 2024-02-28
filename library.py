import json
import os
import subprocess

import numpy as np
import pandas as pd


def run_js_scripts(file_paths):
    processes = []
    for path in file_paths:
        # Form the command to execute 'node' with the file path
        command = ['node', path]
        
        # Spawn a new process for each command
        process = subprocess.Popen(command)
        
        # Append the process to the list of processes
        processes.append(process)

    # Wait for all processes to complete
    for process in processes:
        process.wait()
    print("All processes have completed.")
    return 0


def get_file_paths(directory_path):
    file_paths = []

    if not os.path.exists(directory_path):
        return file_paths
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

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


def find_best_odds(df):
    # Identify all the columns for team1 and team2 odds
    team1_cols = [col for col in df.columns if 'team1' in col]
    team2_cols = [col for col in df.columns if 'team2' in col]
    
    # Function to find the maximum odds and their source, ignoring None values
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
    
    # Select only the relevant columns to display
    cols_to_display = ['match', 'best_team1_odds', 'best_team1_source', 'best_team2_odds', 'best_team2_source']
    return df[cols_to_display]

def arbitrage(row):
    implied_team1 = 1 / float(row['best_team1_odds'])
    implied_team2 = 1 / float(row['best_team2_odds'])
    if implied_team1 + implied_team2 < 1:
        return 1
    return 0

def open_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return np.array(data)
