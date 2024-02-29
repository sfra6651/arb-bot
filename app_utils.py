import numpy as np
import pandas as pd
import streamlit as st

from library import *
from main import *


def stl_card(row, row_num):
    odds_total = float(row['best_team1_odds']) + float(row['best_team2_odds'])
    teams = row['match'].split(' ')
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
        stake = st.number_input('Stake', key=row_num, placeholder='Set stake...', value=None, label_visibility='collapsed')
    with col2:
        if stake:
            st.subheader(f"Profit: $:green[{round(stake * row['%_profit']/100,2)}]")
        else:
            st.subheader(f"Profit: $:green[{0.0}]")

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
            st.write(float(stake) * float(row['best_team2_odds']) / odds_total)
            st.write(float(stake) * float(row['best_team1_odds']) / odds_total)
    #divider
    st.markdown("---")
