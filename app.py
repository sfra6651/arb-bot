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

if "show_arbs" not in st.session_state:
    st.session_state.show_arbs = False

st.set_page_config(layout="wide")
left_margin, main_content, right_margin = st.columns([1, 4, 1])

with main_content:
    st.title("Arb finder")
    if st.button('Show Arbs'):
        st.session_state.show_arbs = True

if st.session_state.show_arbs:
    with main_content:
        if "results" not in st.session_state:
            st.session_state.results = temp_results()

        row_num = 0

        st.write(get_arbs())
        for _, row in st.session_state.results.iterrows():
            stl_card(row, row_num)
            row_num += 1

