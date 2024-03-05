import time

import numpy as np
import pandas as pd
import streamlit as st

from app_utils import *
from library import *
from main import *


def temp_results():
    df = get_arbs()
    duplicated_df = pd.concat([df, df], ignore_index=True)
    duplicated_df = pd.concat([duplicated_df, duplicated_df], ignore_index=True)
    return duplicated_df

if __name__ == '__main__':

    st.set_page_config(layout="wide")

    if "show_arbs" not in st.session_state:
        st.session_state.show_arbs = False

    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False

    left_margin, main_content, right_margin = st.columns([1, 4, 1])

    with main_content:
        st.title("Arbitrage finder")
        event_type = st.selectbox('Event type', ["rugby union", "esports"], placeholder="Choose an event type...", index=None)

        if event_type and not st.session_state.data_loaded:
            progress_bar("pipetest.py")
            st.session_state.data_loaded = True

        if st.session_state.data_loaded:
            if st.button('Show Arbitrage opportunities'):
                    st.session_state.show_arbs = True

    if st.session_state.show_arbs and st.session_state.data_loaded:
        with main_content:

            if "results" not in st.session_state:
                st.session_state.results = temp_results()

            row_num = 0

            st.write(get_arbs())
            for _, row in st.session_state.results.iterrows():
                stl_card(row, row_num)
                row_num += 1

