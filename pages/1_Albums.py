import streamlit as st
import pandas as pd
from main import albums_df



st.set_page_config(page_title="Albums details", page_icon="📈")

#albums_df = pd.read_csv('/home/pipi/PycharmProjects/spotify_streamlit/albums.csv')
albums_df = albums_df.drop(columns=['artist_id', 'album_type'])
st.title('Album details per band')

#drop_down on Band
bands = albums_df['artist_name'].drop_duplicates()
band = st.selectbox('Select a band', bands, index= None)
try:
    if len(band)>0:
        band_scope = albums_df['artist_name']==band
except:
    band_scope = albums_df['artist_name'].isin(list(bands))

# slider for the years
start_year, end_year = st.slider("Select years", 1990, 2024, (2000, 2020))

st.dataframe(albums_df[(band_scope) & ((albums_df['release_date']>=start_year) & (albums_df['release_date']<=end_year) )],
                    hide_index=True, column_order=('artist_name', 'name', 'release_date', 'total_tracks'),
                    column_config = {'release_date': st.column_config.NumberColumn('release_date', format='%d')},
                    width = 800)

