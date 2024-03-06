import time

import numpy as np
import pandas as pd
import streamlit as st

from app_utils import *
from library import *


def temp_results():
    df = get_arbs()
    duplicated_df = pd.concat([df, df], ignore_index=True)
    duplicated_df = pd.concat([duplicated_df, duplicated_df], ignore_index=True)
    return duplicated_df
def temp_results2():
    return get_arbs()

if __name__ == '__main__':

    st.set_page_config(layout="wide")
    
    # st.session_state.data_loaded = {"rugby_union":True, "esports":True} #uncomment to turn of scraping the data

    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = {"rugby_union":False, "esports":False}

    left_margin, main_content, right_margin = st.columns([1, 4, 1])

    with main_content:
        st.title("Arbitrage finder")
        event_type = st.selectbox('Event type', ["rugby_union", "esports"], placeholder="Choose an event type...", index=None)

        #test if we need to run the scraping scripts. Default behavour will be to run them once every session when we select an event
        if event_type and not st.session_state.data_loaded.get(event_type):

            scrape_data("pipetest.py", "")
            st.session_state.data_loaded[event_type] = True

    #only render if event_type selceted
    if event_type:
        #only reder if data is loaded for event type
        if st.session_state.data_loaded[event_type]:
            with main_content:

                #check wether or not we have already done the arbs calculation this session
                if "results" not in st.session_state:
                    st.session_state.results = {event_type: get_arbs(event_type)}
                if event_type not in st.session_state.results:
                    st.session_state.results[event_type] = get_arbs(event_type)

                #finaly render a list of cards for the event type
                row_num = 0
                for _, row in st.session_state.results[event_type].iterrows():
                    stl_card(row, row_num)
                    row_num += 1

