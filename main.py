import streamlit as st
import pandas as pd
import os
import zipfile
import numpy as np
import altair as alt
import plotly.express as px

import base64
from data_processing import *
from components import *

from streamlit_option_menu import option_menu


st.set_page_config(
    page_title="Candidates Resumes Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():

    st.markdown(
        """
        <style>
        .title {
            font-size: 70px;
            font-weight: bold;
            color: #22A2DD;
            margin-bottom: 50px;
            margin-top: 30px;
            text-align :center;
        }
        hr{

        margin-bottom: 50px;
        
        }
        </style>
        <div class="title">Telnet's Resumes Dashboard</div>
        <hr>
        """,
        unsafe_allow_html=True,
    )

    pages = {
        "Scoreboard": Dashboard,
        "Jobs": Jobs,
        "Upload Resumes": Upload_Resumes,
        "Analytics": Analytics,
    }


        # Initialize session state for job list and current job title
    if "job_list" not in st.session_state:
        st.session_state.job_list = initilize_job_list()

    st.sidebar.image("/home/melek/Dashbord-streamlit/sidebarPic.png")

    # 1. as sidebar menu
    with st.sidebar:
        selected = option_menu(
            " Menu",
            ["Scoreboard", "Jobs", "Upload Resumes", "Analytics"],
            icons=["speedometer", "briefcase-fill","cloud-arrow-up-fill","graph-up"],
            menu_icon="cast",
            default_index=0,
                styles={
        "nav-link-selected": {"background-color": "#22A2DD"},
         "container": {"padding": "10!important"}
    }
        )
        st.session_state.current_page = selected

    pages[st.session_state.current_page]()


if __name__ == "__main__":
    main()
