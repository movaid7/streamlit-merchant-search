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

"""
# Merchant Search

Search for merchants by any of the following properties:
"""

# Snowflake Creds
ctx = snowflake.connector.connect(
    user      = st.secrets["user"],
    password  = st.secrets["password"],
    account   = st.secrets["account"],
    warehouse = st.secrets["warehouse"],
    database  = st.secrets["database"],
    schema    = st.secrets["schema"],
    ocsp_response_cache_filename = "/tmp/ocsp_response_cache")


password = st.text_input('Enter password to enable content',type="password")

if password == st.secrets["appPass"]:
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


# cur = ctx.cursor().execute("SELECT \
#     EMAIL,AVG_MONTHLY_VOLUME,FIRST_TRANSACTION_DATE,LAST_TRANSACTION_DATE,IS_VAS_USER,LAST_VAS_TRANSACTION_DATE, \
#     IS_CA_USER,LAST_CA_DATE,HAS_ORIGINAL,HAS_MOVERLITE,HAS_MOVERPRO,HAS_SHAKERDUO,HAS_SHAKERSOLO,HAS_POSTER,\
#     IS_SHOPIFY_USER, SHOPIFY_PAYMENT_GATEWAY,SHOPIFY_PAYMENT_STATUS,APP_VERSION,MERCHANT_ONBOARDED,SHIPPING_STATUS, \
#     UID, CONSIGNMENT_ID, MERCHANT_REFERRAL_CODE, MID, USER_MOBILE_NUMBER, BUSINESS_MOBILE_NUMBER, ALTNUMBER, \
#     SALES_AGENT_EMAIL, CR_RATE, DR_RATE \
#     FROM CONTACT_DETAILS")