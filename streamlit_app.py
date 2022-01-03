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

    search_options = st.sidebar.container()

    with search_options:
    
        geo_picker = st.selectbox('Geo', COUNTRIES.values(), index=len(COUNTRIES) - 1)
        geo_code = get_key_from_value(COUNTRIES, geo_picker)
        
        time_period_picker = st.selectbox('Time range', TIMEFRAMES, index=2)

        search_property_picker = st.selectbox('Search property', ('search', 'images', 'news', 'youtube', 'froogle'))

        if search_property_picker == 'search':
            search_property_picker = ''
                
        # category_picker = st.selectbox('Category', ('Email', 'Home phone', 'Mobile phone'))
    
        

    

# Filters out zero len kwds
non_empty_kwds = [kwd for kwd in kwds if len(kwd) > 0]

# Faudra sans doute mettre ca dans un try/except pour cas ou il n'y a pas de mots clés tappés

df = interest_over_time(non_empty_kwds, geo_code=geo_code, timeframe=time_period_picker, gprop=search_property_picker)
df.drop('isPartial', axis=1, inplace=True)

st.markdown('#')

st.line_chart(df)






