# Push & Deploy as streamlit cloud to check no web bugs
# Build data to use in the average bar chart
# Next check other pytrends available
# Check Altair Advanced multiline tooltip in docs for tooltip closer to real Google Trends

import altair as alt
import streamlit as st
from trends import *

# Used to cache the df conversion
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')


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
export_options = st.sidebar.container()

with search_options:
    
    geo_picker = st.selectbox('Geo', COUNTRIES.values(), index=len(COUNTRIES) - 1)
    geo_code = get_key_from_value(COUNTRIES, geo_picker)
    
    time_period_picker = st.selectbox('Time range', TIMEFRAMES, index=2)
    
    search_property_picker = st.selectbox('Search property', ('search', 'images', 'news', 'youtube', 'froogle'))

    if search_property_picker == 'search':
        search_property_picker = ''
                
    # category_picker = st.selectbox('Category', ('Email', 'Home phone', 'Mobile phone'))
    
        

    

# Filters out zero len kwds

    st.markdown('---')

        
non_empty_kwds = [kwd for kwd in kwds if len(kwd) > 0]

# Faudra sans doute mettre ca dans un try/except pour cas ou il n'y a pas de mots clés tappés


# Only create df if list of kwds is non empty
if len(non_empty_kwds) > 0:

    df = interest_over_time(non_empty_kwds, geo_code=geo_code, timeframe=time_period_picker, gprop=search_property_picker)
    df.drop('isPartial', axis=1, inplace=True)


    # Add date as a column
    source = df.reset_index()
    # Converting to long form tabular data friendly to altair using pandas melt method
    source = source.melt('date', var_name='term', value_name='value')



    base = alt.Chart(source).encode(
        x='date',
        y='value',
        color='term',
        tooltip='value'
        
    )

    line = base.mark_line()
    points = base.mark_point(filled=True, size=40)
    chart = line + points

    # Allows use of tooltip in chart full size/expanded mode
    st.markdown('<style>#vg-tooltip-element{z-index: 1000051}</style>',
                unsafe_allow_html=True)

    st.altair_chart(chart, use_container_width=True)

    # Will be used for export options
    csv = convert_df(df)

    with export_options:
    
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='interest_over_time.csv',
            mime='text/csv',
        )



st.markdown('#')







