import streamlit as st
import pandas as pd
#from main import artist_df

st.set_page_config(page_title="Nova Rock 2025", page_icon="👋")

st.title("Nova Rock 2025")
st.subheader("Bands stats")

artist_df = pd.read_csv('artist_details.csv')
artist_df = artist_df.drop(columns=['ID'])
artist_df = artist_df.rename(columns={'name':'Band', 'genres':'Genres', 'popularity': 'Popularity', 'followers':'Followers'})
artist_df = artist_df[['Band', 'Genres', 'Popularity', 'Followers']]
artist_df['Genres'] = artist_df['Genres'].replace('"','')

genres = artist_df['Genres'].apply(pd.Series)
genres.columns = [f'Genre_{i+1}' for i in genres.columns]
genres.stack().reset_index().rename(columns = {0: 'Genre'})#.drop(columns = 'level_1')
artist_df = pd.concat([artist_df,genres], axis = 1).drop(columns='Genres').fillna('')

artist_genre = artist_df.drop(columns=['Popularity', 'Followers'])
artist_genre = artist_genre.set_index('Band').stack().reset_index()
artist_genre = artist_genre.drop(columns = ['level_1']).rename(columns = {0: 'Genre'})
artist_genre = artist_genre[artist_genre['Genre']!='']
print(artist_genre)

options = st.multiselect(
    "Select your favorite genres",
    list(artist_genre['Genre'].unique()),
    #['rock'],
)

st.dataframe(artist_genre[artist_genre['Genre'].isin(options)], hide_index=True, width = 400)

st.divider()

##############
# Popularity

st.subheader("Bands popularity")

popularity_df = artist_df[['Band','Popularity']]
min_pop = artist_df['Popularity'].min()
max_pop = artist_df['Popularity'].max()


low_pop, high_pop = st.slider("Select a range", min_pop, max_pop, (80, 100))

st.dataframe(popularity_df[(popularity_df['Popularity']>=low_pop) & (popularity_df['Popularity']<=high_pop)],
             hide_index=True, width = 400)

st.divider()
##############
# Followers
st.subheader("Bands followers")

followers_df = artist_df[['Band','Followers']]
min_foll = followers_df['Followers'].astype(int).min()
max_foll = followers_df['Followers'].astype(int).max()

mean_foll = int(followers_df['Followers'].astype(int).mean())

print(followers_df.info())

low_foll, high_foll = st.slider("Select a range", min_foll, max_foll, (mean_foll - 1000000, mean_foll + 1000000))

st.dataframe(followers_df[(followers_df['Followers']>=low_foll) & (followers_df['Followers']<=high_foll)],
             hide_index=True, width = 400)