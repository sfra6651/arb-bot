import time

import numpy as np
import pandas as pd
import streamlit as st

from library import *
from main import *


# Display elements for a single row in the arbitrage dataframe
def stl_card(row, row_num):
    odds_total = float(row['best_team1_odds']) + float(row['best_team2_odds'])
    teams = row['match'].split('.')
    team1, team2 = teams[0], teams[1]
    colour = ":green"
    if row['%_profit'] < 1:
        colour = ":red"
    if row['%_profit'] > 1 and row['%_profit'] < 4:
        colour = ":orange"

    #title
    st.subheader(f"{team1} vs {team2}  ({colour}[{row['%_profit']}%])")

    #input and profit display
    col1, col2 = st.columns(2)
    with col1:
        stake = st.number_input('Stake', key=row_num, placeholder='Set stake...', value=100, label_visibility='collapsed')
        real_bet_options = real_bets([row['team1_implied_odds'], row['team2_implied_odds']], [row['best_team1_odds'], row['best_team2_odds']], stake)
        option = st.selectbox('Real bet options', real_bet_options, key=f"opt{row_num}")
    with col2:
        if stake:
            st.subheader(f"Avg Profit: $:green[{round(stake * row['%_profit']/100,2)}]")
        else:
            st.subheader(f"Avg Profit: $:green[{0.0}]")
        st.write("")
        st.subheader(f"Real Stake: ${colour}[{option[0] + option[1]}.00]")
        # real_return1 = max(option)* min([row['best_team1_odds'], row['best_team2_odds']])
        # real_return2 = min(option)* max([row['best_team1_odds'], row['best_team2_odds']])
        # st.subheader(f"Real returns: \$:green[{round(real_return1, 2)}]  \$:green[{round(real_return2, 2)}]")
    

    # arbitrage opportunity info
    first, second, third, forth = st.columns([1, 1, 1, 1])
    with first:
        st.markdown(f"**{team1}**")
        st.markdown(f"**{team2}**")
    with second:
        st.write(row['best_team1_odds'])
        st.write(row['best_team2_odds'])
    with third:
        s1 = row['best_team1_source'].split('_')[0]
        s2 = row['best_team2_source'].split('_')[0]
        st.write(s1)
        st.write(s2)
    with forth:
        if stake:
            st.write(round(float(option[0]) * row['best_team1_odds'], 2))
            st.write(round(float(option[1]) * row['best_team2_odds'], 2))
    #divider
    st.markdown("---")

def progress_bar(path):

    cmd = ['python', path]

    # Start the process
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    while True:
        # Read one line of output
        line = process.stdout.readline()
        if not line:
            break  # No more output
        # Decode line (from bytes to string) and process it
        progress = line.decode('utf-8').strip()
        if progress.isdigit():
            my_bar.progress(max(0, int(progress) - 5), text=progress_text)

    # Wait for the process to finish and get the exit code
    process.wait()
    my_bar.empty()

