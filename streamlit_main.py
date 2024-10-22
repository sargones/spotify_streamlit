import streamlit as st
import pandas as pd
import streamlit

albums_df = pd.read_csv('albums.csv')
albums_df = albums_df.drop(columns=['artist_id', 'album_type'])
st.title('Album details per band')

#drop_down on Band
bands = albums_df['artist_name'].drop_duplicates()
band = st.selectbox('Select a band', bands)

# slider for the years
start_year, end_year = st.slider("Select a range of values", 1990, 2024, (2000, 2020))

streamlit.dataframe(albums_df[(albums_df['artist_name']==band) & ((albums_df['release_date']>=start_year) & (albums_df['release_date']<=end_year) )],
                    hide_index=True, column_order=('artist_name', 'name', 'release_date', 'total_tracks'),
                    column_config = {'release_date': st.column_config.NumberColumn('release_date', format='%d')},
                    width = 800)
#st.data_editor(albums_df, column_config = {'release_date': st.column_config.NumberColumn('release_date', format='%d')})
