from trends import *
import streamlit as st

st.set_page_config('Google Trends', page_icon=':chart_with_upwards_trend:', layout='wide', initial_sidebar_state='expanded')

st.title(f':chart_with_upwards_trend: Google Trends')

# Initialize kwds array with empty strings
kwds = ['', '', '', '']

col1, col2, col3, col4 = st.columns(4)

with col1:
    kwds[0] = st.text_input('Add a search term', key='kwd1')

with col2:
    kwds[1] = st.text_input('Add a search term', key='kwd2')

with col3:
    kwds[2] = st.text_input('Add a search term', key='kwd3')

with col4:
    kwds[3] = st.text_input('Add a search term', key='kwd4')

    search_options = st.sidebar.form('Search Options')

    with search_options:
    
        geo_picker = st.selectbox('Geo', COUNTRIES.values())
        time_period_picker = st.selectbox('Time range', TIMEFRAMES)
        # category_picker = st.selectbox('Category', ('Email', 'Home phone', 'Mobile phone'))
        # search_property_picker = st.selectbox('Search property', ('Email', 'Home phone', 'Mobile phone'))
    
        filters_submitted = st.form_submit_button("Apply filters")
        
        if filters_submitted:
            df = interest_over_time(non_empty_kwds)

    

# Filters out zero len kwds
non_empty_kwds = [kwd for kwd in kwds if len(kwd) > 0]

# Faudra sans doute mettre ca dans un try/except pour cas ou il n'y a pas de mots clés tappés 
df = interest_over_time(non_empty_kwds)

st.line_chart(df)



df.drop('isPartial', axis=1, inplace=True)

# df.drop('is





