import streamlit as st
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


def Dashboard():
    if "radar_data_scores" not in st.session_state:
        st.session_state.radar_data_scores = [
            0,
            0,
            0,
        ]
    if "radar_data_jobs" not in st.session_state:
        st.session_state.radar_data_jobs = [
            "n",
            "n",
            "n",
        ]

    main_col = st.columns((4.5, 2.5), gap="large")
    with main_col[0]:
        st.markdown(
            """
            <style>
            .custom-selectbox-label {
                font-size: 20px;  /* Adjust font size */
                color: #808080;   /* Set your desired color */
                font-weight: bold;
                display: block;  /* Ensure it appears as a block element */
            }
            </style>
            <div class="custom-selectbox-label">Filter By Job Offer :</div>
        """,
            unsafe_allow_html=True,
        )
        # Display job options
        job = st.selectbox("", options=st.session_state.job_list, key="jobs")

        top_condidates, jobs_critiria, score_list , resumes_pdf_path = get_top_candidates(job)
        # Generate and display a DataFrame with random data

        df = pd.DataFrame(top_condidates)

        event = st.dataframe(
            df,
            on_select="rerun",
            selection_mode="single-row",
            column_config={
                "Resume": st.column_config.LinkColumn("Resume"),
            },
        )

        if len(event.selection["rows"]):
            selected_row = event.selection["rows"][0]
            # print(selected_row)
            index = df.index[selected_row]
            st.session_state["radar_data_scores"] = score_list[index]
            print(score_list[index])
            st.session_state["radar_data_jobs"] = jobs_critiria
            print(jobs_critiria)
            display_resume_pdf(
                resumes_pdf_path[index]
            )

    with main_col[1]:

        df = pd.DataFrame(
            dict(
                r=st.session_state["radar_data_scores"],
                theta=st.session_state["radar_data_jobs"],
            )
        )



        fig = px.line_polar(df, r="r", theta="theta", line_close=True,color_discrete_sequence=px.colors.sequential.Plasma_r,template="plotly_dark")

        fig.update_traces(
            fill="toself",
            fillcolor="rgba(34, 162, 221, 0.4)",
            line_color="rgba(34, 162, 221, 1)",
        )

        # fig.update_layout(
        #     width=400,  # Set width of the chart
        #     height=400,  # Set height of the chart
        #     title="Radar Chart Example",
        #     plot_bgcolor="rgb(255, 255, 0)",  # Red background inside the plotting area
        #     paper_bgcolor="red",
        #     polar_bgcolor="rgb(255, 257, 0)",
        #     polar_radialaxis_gridcolor="#ff0000",
        #     polar_angularaxis_gridcolor="#0000ff",
        #     polar=dict(
        #         bgcolor="rgba(255, 255, 255, 1)",
        #         angularaxis=dict(
        #             tickfont=dict(size=18),  # Increase font size for theta labels
        #             gridcolor="rgb(255, 130, 0)",  # Change angular grid color to blue
        #         ),
        #         radialaxis=dict(
        #             gridcolor="rgb(255, 140, 0)",
        #             visible=True,  # Change radial grid color to red
        #         ),
        #     ),  # Background color of the plotting area
        #     # Background color of the whole figure
        # )

        st.markdown(
            """
            <style>
            .custom-selectbox-label {
                font-size: 20px;  /* Adjust font size */
                color: #808080;   /* Set your desired color */
                font-weight: bold;
                display: block;  /* Ensure it appears as a block element */
            }
            </style>
            <div class="custom-selectbox-label">Stats :</div>
        """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(fig)


def Jobs():
    st.session_state.current_comp = "Add Job"

    if "jobs_df" not in st.session_state:
        st.session_state.jobs_df = pd.DataFrame(get_jobs_list())

    def Add_job():
        main_col = st.columns((1.5,1.5), gap="large")
        with main_col[0]:
            # st.header("Add Job")

            job_title = st.text_input("Job Title")

            skills = st_tags(
                label="skills",
                suggestions=["java", "jee", "python", ".net", "angular", "android"],
                maxtags=1000,
                key="1",
            )

            with st.form(key="add_job_form", border=False):
                adding_job_form(skills,job_title,main_col)

        st.session_state.jobs_df = pd.DataFrame(get_jobs_list())


    def view_delete():
        st.markdown(
            """
        <style>
        .custom-selectbox-label {
            font-size: 20px;  /* Adjust font size */
            color: #808080;   /* Set your desired color */
            font-weight: bold;
            display: block;
            margin-bottom:20px /* Ensure it appears as a block element */
        }
        </style>
        <div class="custom-selectbox-label">Jobs List :</div>
    """,
            unsafe_allow_html=True,
        )



        event = st.dataframe(
            st.session_state.jobs_df,
            on_select="rerun",
            selection_mode="multi-row",
            column_config={
                "Resume": st.column_config.LinkColumn("Resume"),
            },
        )
        if len(event.selection["rows"]):
            selected_rows = event.selection["rows"]


        if st.button("Delete"):
            if len(event.selection["rows"]):
                rows_to_delete = st.session_state.jobs_df.iloc[selected_rows]
                for index, row in rows_to_delete.iterrows():
                    delete_document("jobs", {"job_title.field": row["job_title"]})
                    # delete_document("scoring", {"job_title.field": row["job_title"]})
                    st.session_state["job_list"].remove(row["job_title"])

                # Delete the selected rows from the DataFrame
                st.session_state.jobs_df.drop(selected_rows, inplace=True)
                # Reset the index after deletion
                st.session_state.jobs_df.reset_index(drop=True, inplace=True)
                st.rerun()  
            else:
                st.write("No rows selected for deletion.")


    pages = {
        "Add Job": Add_job,
        "View/Delete Jobs": view_delete,
    }

    selected2 = option_menu(None, ["Add Job", "View/Delete Jobs"], 
    icons=['file-earmark-plus', 'trash-fill'], 
    menu_icon="cast", default_index=0, orientation="horizontal"  ,              styles={
        "nav-link-selected": {"background-color": "#22A2DD"},
    })
    st.session_state.current_comp =selected2

    
    pages[st.session_state.current_comp]()




def Upload_Resumes():
    st.header("Upload Resumes Folder ")

    uploaded_folder = st.file_uploader("Choose a ZIP file", type=["zip"])
    if uploaded_folder:
        post_process_upload_resues_ZIP(uploaded_folder)



def Analytics():

    st.markdown(
        """
        <style>
        .header {
            font-size: 20px;  /* Adjust font size as needed */
            color:#808080;   /* Set your desired color here */
            font-weight: bold;
        }
        .metrics-container {
            text-align: center; 
        }
        </style>
        <div class="header">JOBS/RESUMES</div>
    """,
        unsafe_allow_html=True,
    )

    migrations_col = st.columns((0.2, 1, 0.2))
    with migrations_col[1]:

        # Display metrics
        st.metric(label="TOTAL JOBS", value=23)
        st.metric(label="TOTAL RESUMES", value=240)

    st.markdown(
        """
        <style>
        .header {
            font-size: 30px;  /* Adjust font size as needed */
            color:#808080;   /* Set your desired color here */
            font-weight: bold;
            margin-bottom:10px;
        }
        </style>
        <div class="header">STATISTICS</div>
    """,
        unsafe_allow_html=True,
    )

    donut_chart_greater = make_donut(30, "AVRG candidate score", "green")
    donut_chart_less = make_donut(10, "AVRG score per job", "red")

    migrations_col = st.columns((0.2, 1, 0.2))
    with migrations_col[1]:
        st.write("AVRG candidate score")
        st.altair_chart(donut_chart_greater)
        st.write("AVRG score per job ")
        st.altair_chart(donut_chart_less)
    pass


