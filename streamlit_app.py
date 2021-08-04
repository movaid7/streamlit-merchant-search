from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import snowflake
import snowflake.connector
import boto3

st.set_page_config(
    page_title="Merchant Search",
    page_icon="🔎",
    layout="wide"
    )

# Snowflake Creds
ctx = snowflake.connector.connect(
    user      = st.secrets["user"],
    password  = st.secrets["password"],
    account   = st.secrets["account"],
    warehouse = st.secrets["warehouse"],
    database  = st.secrets["database"],
    schema    = st.secrets["schema"],
    ocsp_response_cache_filename = "/tmp/ocsp_response_cache")

password = st.text_input('Enter password to enable content', type="password", help ='Request access if needed')

if password == st.secrets["appPass"]:

    """
    # Merchant Search

    Search for merchants by any of the following properties:
    """
    # Search Widget
    searchOption = st.radio('', ['UID','MERCHANT_ID','Email','Name','Surname','Trading_Name','Mobile_Number'])
    st.subheader(f'Search by {searchOption}')
    searchText,sql = '',''
    numResults = 1
    if searchOption in ('Email','Name','Surname','Trading_Name','Mobile_Number'):   
        searchText = st.text_input('')
        sql= st.secrets["sql"] + f"{searchOption} LIKE '%{searchText}%'"
        # numResults = 30
        numResults = st.slider('Number of results returned', min_value=10, max_value=100)
    else:
        searchText = st.number_input('',value=0, min_value=0)
        sql = st.secrets["sql"] + f"{searchOption} = {searchText}"
    st.markdown("***")
    st.text(" \n")

    # Fetch & Display Results
    cur = ctx.cursor().execute(sql)
    ret = cur.fetchmany(numResults)
    if len(ret) > 1 and searchText != '':
        df = pd.DataFrame(ret)
        df.columns = st.secrets["columns"]
        st.table(df)
    elif len(ret) == 1 and searchText != '':
        df = pd.DataFrame(ret)
        df.columns = st.secrets["columns"]
        st.table(df)
    else:
        st.subheader("No Results")
